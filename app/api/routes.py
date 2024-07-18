from typing import Optional
import secrets

from flask import (
    Flask,
    jsonify,
    request,
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user,
    logout_user,
)

from flask_wtf.csrf import CSRFProtect, generate_csrf

from resources import actions
from objects import UserSession


app = Flask(__name__)
app.config.update(
    SECRET_KEY=secrets.token_hex(),
    SESSION_COOKIE_HTTPONLY=True,
    REMEMBER_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Strict",
)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

csrf = CSRFProtect(app)


@app.route("/api/testRoute", methods=["GET"])
def test_route():
    return jsonify({"Success": True}), 200


@app.route("/api/getcsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response


@login_manager.user_loader
def user_loader(user_id: str) -> Optional[UserSession]:
    user = actions.get_user_from_id(user_id)
    if user:
        return UserSession(user_id)
    return None


@app.route("/api/signup", methods=["POST"])
def signup():
    signup_data = request.json
    user_email = signup_data.get("user_email")
    password = signup_data.get("password")
    first_name = signup_data.get("first_name")
    last_name = signup_data.get("last_name")

    try:
        user = actions.add_user(
            user_email, password, first_name=first_name, last_name=last_name
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({user.get_dict()}), 201


@app.route("/api/login", methods=["POST"])
def login():
    import hashlib

    login_data = request.json
    print(f"login_data: {login_data}")
    user_email = login_data.get("userEmail")
    password = login_data.get("password")

    user = actions.get_user_from_email(user_email=user_email)
    login_status = False
    print(f"User: {user}")
    if not user:
        return jsonify({"login": login_status, "message": "User not found"}), 404
    try:
        assert hashlib.sha256(password.encode()).hexdigest() == user.password
    except AssertionError:
        return jsonify({"login": login_status}), 401
    user_session = UserSession(user.get_id())
    login_user(user_session)
    login_status = True
    return jsonify({"login": login_status}), 200


@app.route("/api/getsession")
def check_session():
    if current_user.is_authenticated:
        return jsonify({"login": True})

    return jsonify({"login": False})


@app.route("/api/logout")
def logout():
    logout_user()
    return jsonify({"logout": True}), 200


@app.route("/api/user")
@login_required
def user():
    return jsonify(current_user.get_id()), 200
