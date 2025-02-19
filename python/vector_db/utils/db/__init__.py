from .base import BaseVectorDB
from .postgres import PostgresVectorDB


# Factory to get appropriate DB implementation
def get_vector_db(db_type: str, user_id: int) -> BaseVectorDB:
    if db_type == "postgres":
        return PostgresVectorDB(user_id)
    else:
        raise ValueError(f"Unsupported vector database type: {db_type}")
