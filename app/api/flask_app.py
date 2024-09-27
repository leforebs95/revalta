import logging
import os
import secrets

from sqlalchemy.orm import DeclarativeBase

# Flask Imports
from flask import Flask, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
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

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app():

    env_vars = get_config()

    db_vars = env_vars["db"]

    app = Flask(__name__)
    app.config["CORS_HEADERS"] = "Content-Type"
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Use an environment variable for the secret key
    secret_key = os.environ.get("FLASK_SECRET_KEY")

    app.config.update(
        SECRET_KEY=secret_key,
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{db_vars['username']}:{db_vars['password']}@{db_vars['host']}/{db_vars['db-name']}",
    )

    csrf.init_app(app)

    @app.route("/api/getcsrf", methods=["GET"])
    def get_csrf():
        logger.info(f'Secret key: {app.config.get("SECRET_KEY")}')
        token = generate_csrf()
        logger.info(f"Generated Token: {token}")
        response = jsonify({"detail": "CSRF Header set"})
        response.headers.set("X-CSRFToken", token)
        return response

    @app.route("/api/validatecsrf", methods=["POST"])
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

    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    bcrypt.init_app(app)

    # from models import User

    from session import register_session_routes

    register_session_routes(app, login_manager, db, bcrypt, logger)

    migrate = Migrate(app, db)

    return app
