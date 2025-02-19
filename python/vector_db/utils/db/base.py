from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import uuid


class BaseVectorDB(ABC):
    def __init__(self, user_id: int):
        self.user_id = user_id

    @abstractmethod
    def initialize_user_schema(self):
        """Initialize storage for a new user"""
        pass

    @abstractmethod
    def insert_document(self, text: str, chunks: List[Dict]) -> uuid.UUID:
        """Insert a document and its chunks with embeddings"""
        pass

    @abstractmethod
    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        score_threshold: Optional[float] = None,
    ) -> List[Dict]:
        """Find k most similar chunks"""
        pass

    @abstractmethod
    def keyword_search(self, keyword: str, k: int = 5) -> List[Dict]:
        """Find chunks containing keyword"""
        pass

    @abstractmethod
    def get_document(self, document_id: uuid.UUID) -> Optional[Dict]:
        """Get document and all its chunks"""
        pass
