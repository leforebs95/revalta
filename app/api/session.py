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

from models import User


def register_session_routes(app, login_manager, db, bcrypt, logger):

    @app.route("/api/version", methods=["GET"])
    def version():
        return jsonify({"version": "0.0.1"})

    @app.route("/api/signup", methods=["POST"])
    def signup():
        signup_data = request.json
        user_email = signup_data.get("userEmail")
        password = signup_data.get("password")
        first_name = signup_data.get("firstName")
        last_name = signup_data.get("lastName")

        logger.info(
            f"Creating user with {user_email}, {password}, {first_name}, {last_name}"
        )
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
        login_data = request.json
        logger.info(f"login_data: {login_data}")
        user_email = login_data.get("userEmail")
        password = login_data.get("password")

        login_status = False
        user = User.query.filter_by(user_email=user_email).first()
        logger.info(f"User: {user}")
        if user is None:
            return jsonify({"login": login_status, "message": "Invalid User"}), 401
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            login_status = True
        else:
            return jsonify({"login": login_status, "message": "Invalid Password"}), 401
        return jsonify({"login": login_status, "user": user.to_json()}), 200

    @app.route("/api/getsession")
    def check_session():
        logger.info(f"Checking session for: {current_user}")
        if current_user.is_authenticated:
            logger.info(f"Current user active: {current_user.user_email}")
            return jsonify({"login": True})
        logger.info("No current user active")
        return jsonify({"login": False})

    @app.route("/api/logout")
    @login_required
    def logout():
        logger.info(f"Logging out user: {current_user}")
        logout_user()
        return jsonify({"logout": True}), 200
