from typing import Optional
import secrets

from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    redirect,
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
app.secret_key = secrets.token_hex()
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
    username = signup_data.get("username")
    password = signup_data.get("password")
    email = signup_data.get("email")

    try:
        user = actions.add_user(username, password, email)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({user.get_dict()}), 201


@app.route("/api/login", methods=["POST"])
def login():
    import hashlib

    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")

    user = actions.get_user_from_username(username=username)
    login_status = False
    if not user:
        return jsonify({"login": login_status}), 404
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
