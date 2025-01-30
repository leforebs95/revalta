from datetime import datetime
from datetime import timezone

from flask import jsonify, request, current_app, redirect, url_for
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)

from werkzeug.exceptions import BadRequest, Unauthorized
from email_validator import validate_email, EmailNotValidError
from http import HTTPStatus
from urllib.parse import urlencode
import secrets
import requests

from . import auth
from app.models import db

from app import logger
from app import bcrypt

from app.models import User
from utils.dynamo_db import OAuthStateStore


@auth.route("/api/auth/version", methods=["GET"])
def version():
    return jsonify({"version": "0.0.1"})


@auth.route("/api/auth/signup", methods=["POST"])
def signup():
    try:
        # Get JSON data or raise error if not JSON
        signup_data = request.get_json()
        if not signup_data:
            raise BadRequest("Missing JSON data")

        # Extract fields with validation
        required_fields = ["userEmail", "password", "firstName", "lastName"]
        if not all(field in signup_data for field in required_fields):
            raise BadRequest("Missing required fields")

        user_email = signup_data["userEmail"]
        password = signup_data["password"]
        first_name = signup_data["firstName"]
        last_name = signup_data["lastName"]

        # Validate email format
        try:
            valid = validate_email(user_email)
            user_email = valid.email
        except EmailNotValidError as e:
            return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

        # Validate password strength
        if len(password) < 8:
            return (
                jsonify({"error": "Password must be at least 8 characters long"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Check for existing user
        if User.query.filter_by(user_email=user_email).first():
            return jsonify({"error": "Email already registered"}), HTTPStatus.CONFLICT

        # Create new user
        try:
            hashed_password = bcrypt.generate_password_hash(password)
            user = User(
                user_email=user_email,
                first_name=first_name[:50],  # Limit field lengths
                last_name=last_name[:50],
                password=hashed_password,
                is_email_verified=False,
            )
            db.session.add(user)
            db.session.commit()

            # Log success without sensitive data
            logger.info(f"New user registered: {user_email}")

            return jsonify(user.to_json()), HTTPStatus.CREATED

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {str(e)}")
            return (
                jsonify({"error": "Error creating user account"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    except BadRequest as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST


@auth.route("/api/auth/login", methods=["POST"])
def login():
    try:
        login_data = request.get_json()
        if not login_data:
            raise BadRequest("Missing JSON data")
        logger.info(f"Login attempt: {login_data}")
        user_email = login_data.get("userEmail", "").lower()
        password = login_data.get("password")

        if not user_email or not password:
            raise BadRequest("Email and password are required")

        user = User.query.filter_by(user_email=user_email).first()

        if user is None or not bcrypt.check_password_hash(user.password, password):
            # Use same message for both cases to prevent email enumeration
            raise Unauthorized("Invalid credentials")

        if user.is_deleted:
            raise Unauthorized("Account has been deactivated")

        login_user(user, fresh=True, remember=True)

        # Update last login time
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify({"login": True, "user": user.to_json()}), HTTPStatus.OK

    except (BadRequest, Unauthorized) as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@auth.route("/api/auth/oauth2/authorize/<provider>", methods=["GET"])
def oauth2_authorize(provider):
    # Generate state token and timestamp
    try:
        if not current_user.is_anonymous:
            logger.info(
                f"Already authenticated user attempting OAuth: {current_user.user_email}"
            )
            return jsonify({"error": "Already authenticated"}), HTTPStatus.BAD_REQUEST

        provider_data = current_app.config.get("OAUTH2_PROVIDERS", {}).get(provider)
        if provider_data is None:
            logger.error(f"Invalid OAuth provider requested: {provider}")
            return jsonify({"error": "Invalid OAuth provider"}), HTTPStatus.NOT_FOUND

        state_token = secrets.token_urlsafe(32)
        state_store = OAuthStateStore(current_app.config["ENVIRONMENT"])

        # Store state in DynamoDB
        if not state_store.store_state(state_token, provider):
            return (
                jsonify({"error": "Unable to initiate OAuth flow"}),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        # Build authorization URL
        oauth_params = {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "auth.oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": state_token,
        }

        authorization_url = (
            f"{provider_data['authorize_url']}?{urlencode(oauth_params)}"
        )
        logger.info(f"Initiating OAuth flow for provider: {provider}")

        return (
            jsonify(
                {
                    "authorizationUrl": authorization_url,
                    "provider": provider,
                    **oauth_params,
                }
            ),
            HTTPStatus.OK,
        )

    except Exception as e:
        logger.error(f"OAuth authorization error: {str(e)}")
        return (
            jsonify({"error": "Authentication service unavailable"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@auth.route("/api/auth/oauth2/callback/<provider>")
def oauth2_callback(provider):
    try:
        state_token = request.args.get("state")
        if not state_token:
            return jsonify({"error": "Missing state parameter"}), HTTPStatus.BAD_REQUEST

        state_store = OAuthStateStore(current_app.config["ENVIRONMENT"])
        stored_state = state_store.get_state(state_token)
        if not stored_state:
            return (
                jsonify({"error": "Invalid or expired state"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Validate provider matches
        if stored_state["provider"] != provider:
            logger.error(
                f"Provider mismatch. Expected: {stored_state['provider']}, Got: {provider}"
            )
            return jsonify({"error": "Invalid OAuth provider"}), HTTPStatus.UNAUTHORIZED

        # Clean up used state
        state_store.delete_state(state_token)

        if not current_user.is_anonymous:
            logger.info(
                f"Already authenticated user in OAuth callback: {current_user.user_email}"
            )
            return jsonify({"error": "Already authenticated"}), HTTPStatus.BAD_REQUEST

        provider_data = current_app.config.get("OAUTH2_PROVIDERS", {}).get(provider)
        if provider_data is None:
            logger.error(f"Invalid OAuth provider in callback: {provider}")
            return jsonify({"error": "Invalid OAuth provider"}), HTTPStatus.NOT_FOUND

        # Validate error response
        if "error" in request.args:
            error_details = {
                k: v for k, v in request.args.items() if k.startswith("error")
            }
            logger.error(f"OAuth error response: {error_details}")
            return (
                jsonify({"error": "Authentication failed", "details": error_details}),
                HTTPStatus.BAD_REQUEST,
            )

        # Validate state parameter
        if request.args.get("state") != stored_state["item_id"]:
            logger.error("OAuth state mismatch")
            logger.error(f"Expected: {stored_state['item_id']}")
            logger.error(f"Received: {request.args.get('state')}")
            return (
                jsonify({"error": "Invalid state parameter"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Validate authorization code
        if "code" not in request.args:
            logger.error("Missing authorization code")
            return (
                jsonify({"error": "Missing authorization code"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Exchange code for token
        token_response = requests.post(
            provider_data["token_url"],
            data={
                "client_id": provider_data["client_id"],
                "client_secret": provider_data["client_secret"],
                "code": request.args["code"],
                "grant_type": "authorization_code",
                "redirect_uri": url_for(
                    "auth.oauth2_callback", provider=provider, _external=True
                ),
            },
            headers={"Accept": "application/json"},
        )

        if token_response.status_code != 200:
            logger.error(f"Token exchange failed: {token_response.text}")
            return jsonify({"error": "Token exchange failed"}), HTTPStatus.UNAUTHORIZED

        oauth2_token = token_response.json().get("access_token")
        if not oauth2_token:
            logger.error("No access token in response")
            return (
                jsonify({"error": "No access token received"}),
                HTTPStatus.UNAUTHORIZED,
            )

        # Get user info
        userinfo_response = requests.get(
            provider_data["userinfo"]["url"],
            headers={
                "Authorization": f"Bearer {oauth2_token}",
                "Accept": "application/json",
            },
        )

        if userinfo_response.status_code != 200:
            logger.error(f"Failed to get user info: {userinfo_response.text}")
            return (
                jsonify({"error": "Failed to get user info"}),
                HTTPStatus.UNAUTHORIZED,
            )

        user_email = provider_data["userinfo"]["email"](userinfo_response.json())

        # Find or create user
        user = User.query.filter_by(user_email=user_email).first()
        if user is None:
            user = User(
                user_email=user_email,
                first_name=user_email.split("@")[0],  # Default to email username
                last_name="",
                password=bcrypt.generate_password_hash(secrets.token_urlsafe(32)),
                is_email_verified=True,  # OAuth verified
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new user via OAuth: {user_email}")
        else:
            logger.info(f"Existing user logged in via OAuth: {user_email}")

        # Log the user in
        login_user(user, fresh=True, remember=True)
        user.last_login = datetime.now(timezone.utc)
        db.session.commit()

        # return jsonify({"login": True, "user": user.to_json()}), HTTPStatus.OK
        return redirect("/dashboard")

    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return (
            jsonify({"error": "Authentication failed"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@auth.route("/api/auth/getsession")
def check_session():
    if current_user.is_authenticated:
        logger.info(f"Current user active: {current_user.user_email}")
        return jsonify({"login": True, "user": current_user.to_json()})
    logger.info("No current user active")
    return jsonify({"login": False})


@auth.route("/api/auth/logout", methods=["POST"])
@login_required
def logout():
    try:
        user_email = current_user.user_email  # Store before logout
        logout_user()
        current_app.logger.info(f"User logged out: {user_email}")
        return jsonify({"logout": True}), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
