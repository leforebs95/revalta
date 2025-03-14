import os
import secrets


class LocalFlaskConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://local_vector_user:local_vector_pass@local-vector-db:5432/local_vector_db"
    )
    DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    VECTOR_DIMENSION = 384
