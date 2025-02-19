from abc import ABC, abstractmethod
from typing import List


class BaseEmbedder(ABC):
    """Abstract base class for text embedding models"""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Convert text into vector embedding"""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Convert batch of texts into vector embeddings"""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension"""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return model identifier"""
        pass
