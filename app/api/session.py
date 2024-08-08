from flask import (
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

from models import User


def register_session_routes(app, db, bcrypt):

    @app.route("/api/signup", methods=["POST"])
    def signup():
        signup_data = request.json
        user_email = signup_data.get("userEmail")
        password = signup_data.get("password")
        first_name = signup_data.get("firstName")
        last_name = signup_data.get("lastName")

        print(f"Creating user with {user_email}, {password}, {first_name}, {last_name}")
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(
            user_email=user_email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            is_email_verified=False,
        )
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_json()), 201

    @app.route("/api/login", methods=["POST"])
    def login():
        import hashlib

        login_data = request.json
        print(f"login_data: {login_data}")
        user_email = login_data.get("userEmail")
        password = login_data.get("password")

        user = User.query.filter_by(user_email=user_email).first()
        login_status = False
        print(f"User: {user}")
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            login_status = True
        else:
            return jsonify({"login": login_status, "message": "Invalid Password"}), 401
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
