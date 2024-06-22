import secrets

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user,
    logout_user,
)
from markupsafe import escape

# from flask_bcrypt import bcrypt
from resources import data


app = Flask(__name__)
app.secret_key = secrets.token_hex()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return data.get_user_from_id(user_id=user_id)


@app.route("/")
def landing_page():
    return render_template("index.html")


def perform_signup(username, password, email):
    try:
        user = data.add_user(username, password, email)
    except ValueError as e:
        return f"<p>Failed to create user: {e}</p>"

    login_user(user)
    user.set_is_authenticated(True)
    return redirect("/dashboard")


def show_signup_form():
    return render_template("signup_form.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return perform_signup(
            request.form["username"], request.form["password"], request.form["email"]
        )
    else:
        return show_signup_form()


def perform_login(username, password):
    import hashlib

    user = data.get_user_from_username(username=username)
    if not user:
        return f"<p>User {username} not found</p>"
    try:
        assert hashlib.sha256(password.encode()).hexdigest() == user.password
    except AssertionError:
        return "<p>Invalid password</p>"
    login_user(user)
    user.set_is_authenticated(True)
    return redirect("/dashboard")


def show_login_form():
    return render_template("login_form.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return perform_login(request.form["username"], request.form["password"])
    else:
        return show_login_form()


@app.route("/logout")
def logout():
    current_user.set_is_authenticated(False)
    logout_user()
    return redirect("/")


@app.route("/dashboard")
@login_required
def dashboard():
    print(f"Current User: {current_user.get_json()}")
    return render_template("dashboard.html", current_user=current_user)
