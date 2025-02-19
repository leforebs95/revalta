import os
import secrets


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://local_uploads_user:local_uploads_pass@local-uploads-db:3306/uploads_db"
    UPLOAD_DIRECTORY = "/usr/src/uploads/uploads"
    MAX_CONTENT_LENGTH = 536_870_912  # 512MB in bytes
    REDIS_HOST = "redis"
    REDIS_PORT = 6379
