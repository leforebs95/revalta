# llm_clients/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseLLMClient(ABC):
    """Base class for LLM API clients."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM based on the prompt."""
        pass

    @abstractmethod
    def generate_with_context(
        self, prompt: str, context: List[Dict[str, str]], **kwargs
    ) -> str:
        """Generate a response using additional context messages."""
        pass
