import os
import logging

from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf


cors = CORS()
csrf = CSRFProtect()
bcrypt = Bcrypt()

migrate = Migrate()
login_manager = LoginManager()


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app():

    app = Flask(__name__)

    if aws_env := os.getenv("AWS"):
        if aws_env == "PROD":
            app.config.from_object("config.ProdFlaskConfig")
        elif aws_env == "PREPROD":
            app.config.from_object("config.PreProdFlaskConfig")
        elif aws_env == "DEV":
            app.config.from_object("config.DevFlaskConfig")
        else:
            raise ValueError(f"Invalid AWS environment: {aws_env}")
    else:
        logger.info("No AWS environment detected. Using local configuration.")
        app.config.from_object("config.LocalFlaskConfig")

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:3000"],
                "supports_credentials": True,
                "allow_headers": ["Content-Type", "X-CSRFToken"],
                "max_age": 3600,
            }
        },
    )

    @app.route("/api/auth/getcsrf", methods=["GET"])
    def get_csrf():
        token = generate_csrf()
        response = jsonify({"detail": "CSRF Header set"})
        response.headers.set("X-CSRFToken", token)
        return response

    @app.route("/api/auth/validateCsrf", methods=["POST"])
    @csrf.exempt
    def validate_csrf_token():
        token = request.headers.get("X-CSRFToken")
        logger.info(f"Received Token: {token}")
        try:
            validate_csrf(token)
        except ValidationError as e:
            return jsonify({"valid": False}), 200
        return jsonify({"valid": True}), 200

    @login_manager.user_loader
    def user_loader(user_id: str):
        from .models import User

        user = User.query.get(int(user_id))
        return user

    bcrypt.init_app(app)
    csrf.init_app(app)

    from .models import db

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)

    login_manager.init_app(app)

    from .auth_api import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    return app
