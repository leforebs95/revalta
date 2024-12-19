from typing import Optional
from urllib.parse import quote_plus
from datetime import timedelta
import logging
import os
import secrets

from sqlalchemy.orm import DeclarativeBase

# Flask Imports
from dynamo_db import DynamoDBStore
from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_login import LoginManager
from wtforms.csrf.core import ValidationError
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from flask_migrate import Migrate

from environment import get_config


class Base(DeclarativeBase):
    pass


bcrypt = Bcrypt()
csrf = CSRFProtect()
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def get_flask_secret(environment: str) -> Optional[str]:
    store = DynamoDBStore(environment)
    secret_data = store.get_item(
        item_type="app_secret", item_id="flask_secret_key", check_ttl=False
    )
    return secret_data.get("value") if secret_data else None


def create_app():

    env_vars = get_config()

    db_vars = env_vars["db"]
    oauth_vars = env_vars["oauth"]

    app = Flask(__name__)
    app.config["CORS_HEADERS"] = "Content-Type"
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": env_vars.get(
                    "ALLOWED_ORIGINS", "http://localhost:3000"
                ).split(","),
                "supports_credentials": True,
                "allow_headers": ["Content-Type", "X-CSRFToken"],
                "max_age": 3600,
            }
        },
    )

    # Use an environment variable for the secret key
    secret_key = get_flask_secret("preprod")

    encoded_password = quote_plus(db_vars["password"].encode("utf8"))
    encoded_username = quote_plus(db_vars["username"].encode("utf8"))
    # Try this connection string format
    connection_url = (
        f"{db_vars['engine']}+pymysql://{encoded_username}:{encoded_password}@"
        f"{db_vars['host']}:{db_vars['port']}/{db_vars['db-name']}"
        "?charset=utf8mb4&binary_prefix=true"
    )

    logger.info(f"Connecting to DB at: {connection_url.split('@')[1]}")

    app.config.update(
        SECRET_KEY=secret_key,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SESSION_COOKIE_SECURE=True,
        PERMANENT_SESSION_LIFETIME=timedelta(days=1),
        SQLALCHEMY_DATABASE_URI=connection_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "pool_size": 10,
            "pool_recycle": 3600,
            "pool_pre_ping": True,
        },
        ENVIRONMENT="preprod",
    )

    app.config.update(
        OAUTH2_PROVIDERS={
            # Google OAuth 2.0 documentation:
            # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
            "google": {
                "client_id": oauth_vars["google_client_id"],
                "client_secret": oauth_vars["google_client_secret"],
                "authorize_url": "https://accounts.google.com/o/oauth2/auth",
                "token_url": "https://accounts.google.com/o/oauth2/token",
                "userinfo": {
                    "url": "https://www.googleapis.com/oauth2/v3/userinfo",
                    "email": lambda json: json["email"],
                },
                "scopes": ["https://www.googleapis.com/auth/userinfo.email"],
            }
        }
    )

    csrf.init_app(app)

    @app.route("/api/getcsrf", methods=["GET"])
    def get_csrf():
        token = generate_csrf()
        response = jsonify({"detail": "CSRF Header set"})
        response.headers.set("X-CSRFToken", token)
        return response

    @app.route("/api/validateCsrf", methods=["POST"])
    @csrf.exempt
    def validate_csrf_token():
        token = request.headers.get("X-CSRFToken")
        logger.info(f"Received Token: {token}")
        try:
            validate_csrf(token)
        except ValidationError as e:
            return jsonify({"valid": False}), 200
        return jsonify({"valid": True}), 200

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    bcrypt.init_app(app)

    from models import User

    @login_manager.user_loader
    def user_loader(user_id: str) -> User:
        logger.info(f"Loading user: {user_id}")
        user = User.query.get(int(user_id))
        logger.info(f"Found user: {user.user_email}")
        return user

    from auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from symptoms import symptoms as symptoms_blueprint

    app.register_blueprint(symptoms_blueprint)

    from lab_results import lab_results as lab_results_blueprint

    app.register_blueprint(lab_results_blueprint)

    # Migrate(app, db)

    return app
