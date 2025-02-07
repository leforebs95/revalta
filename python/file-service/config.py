import os
import secrets


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://local_file_user:local_file_pass@local-file-db:3306/file_db"
    )
    UPLOAD_DIRECTORY = "/usr/src/file-service/uploads"
    MAX_CONTENT_LENGTH = 536_870_912  # 512MB in bytes
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
