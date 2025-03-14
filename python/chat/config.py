import os
from dotenv import load_dotenv

load_dotenv()


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://local_chat_user:local_chat_pass@local-chat-db:5432/chat_db"
    )
    VECTOR_API_URL = os.environ.get("VECTOR_API_URL", "http://vector-api:5003")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")


class DevFlaskConfig(LocalFlaskConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class PreProdFlaskConfig(LocalFlaskConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class ProdFlaskConfig(LocalFlaskConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") 