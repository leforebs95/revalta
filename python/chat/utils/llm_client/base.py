from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union, AsyncGenerator

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        context: Optional[str] = None,
        stream: bool = False
    ) -> Union[str, AsyncGenerator[str, None]]:
        """Generate a chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            context: Optional context string to include in the prompt
            stream: Whether to stream the response
            
        Returns:
            Either a string response or an async generator of response chunks
        """
        pass 