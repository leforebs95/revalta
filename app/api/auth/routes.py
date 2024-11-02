from flask import jsonify, request, current_app
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)
from werkzeug.exceptions import BadRequest, Unauthorized
from email_validator import validate_email, EmailNotValidError
from http import HTTPStatus

from . import auth
from flask_app import db

from flask_app import logger
from flask_app import bcrypt

from models import User


@auth.route("/api/version", methods=["GET"])
def version():
    return jsonify({"version": "0.0.1"})


@auth.route("/api/signup", methods=["POST"])
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


@auth.route("/api/login", methods=["POST"])
def login():
    try:
        login_data = request.get_json()
        if not login_data:
            raise BadRequest("Missing JSON data")

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
        user.last_login = datetime.utcnow()
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


@auth.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        logger.info(f"Current user active: {current_user.user_email}")
        return jsonify({"login": True})
    logger.info("No current user active")
    return jsonify({"login": False})


@auth.route("/api/logout")
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
