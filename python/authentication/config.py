import os
import secrets


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://local_auth_user:local_auth_pass@local-auth-db:3306/auth"
    )
    OAUTH2_PROVIDERS = {
        # Google OAuth 2.0 documentation:
        "google": {
            # https://developers.google.com/identity/protocols/oauth2/web-server#httprest
            "client_id": None,
            "client_secret": None,
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "userinfo": {
                "url": "https://www.googleapis.com/oauth2/v3/userinfo",
                "email": lambda json: json["email"],
            },
            "scopes": ["https://www.googleapis.com/auth/userinfo.email"],
        },
        "azure": {
            "client_id": None,
            "client_secret": None,
            "authorize_url": "https://login.microsoftonline.com/6a8c0988-6adc-4771-bf76-46fc164061a0/oauth2/v2.0/authorize",
            "token_url": "https://login.microsoftonline.com/6a8c0988-6adc-4771-bf76-46fc164061a0/oauth2/v2.0/token",
            "userinfo": {
                "url": "https://graph.microsoft.com/v1.0/me",
                "email": lambda json: json["mail"],
            },
            "scopes": ["User.Read"],
        },
    }
