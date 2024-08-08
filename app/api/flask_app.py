import secrets

from sqlalchemy.orm import DeclarativeBase

# Flask Imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_migrate import Migrate

from environment import get_config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app():

    env_vars = get_config()

    db_vars = env_vars["db"]

    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=secrets.token_hex(),
        SESSION_COOKIE_HTTPONLY=True,
        REMEMBER_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Strict",
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{db_vars['username']}:{db_vars['password']}@{db_vars['host']}/{db_vars['db-name']}",
    )

    csrf = CSRFProtect(app)

    @app.route("/api/getcsrf", methods=["GET"])
    def get_csrf():
        token = generate_csrf()
        response = jsonify({"detail": "CSRF cookie set"})
        response.headers.set("X-CSRFToken", token)
        return response

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    bcrypt = Bcrypt(app)

    from models import User

    @login_manager.user_loader
    def user_loader(user_id: str) -> User:
        return User.query.get(user_id)

    from session import register_session_routes

    register_session_routes(app, db, bcrypt)

    migrate = Migrate(app, db)

    return app
