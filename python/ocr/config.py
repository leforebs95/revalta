import os
import secrets

from dotenv import load_dotenv

load_dotenv()


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://local_ocr_user:local_ocr_pass@local-ocr-db:5432/ocr_db"
    )
    PAGES_LOCATION = "/usr/src/ocr-service/pages"
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
