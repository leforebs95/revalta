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
    UPLOADS_API_URL = os.environ.get("UPLOADS_API_URL", "http://uploads-api:5001")
    VECTOR_API_URL = os.environ.get("VECTOR_API_URL", "http://vector-api:5003")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
