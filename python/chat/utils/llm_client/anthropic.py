from typing import List, Dict, Optional, Union, AsyncGenerator
import anthropic
from flask import current_app

from .base import BaseLLMClient

class AnthropicClient(BaseLLMClient):
    """Anthropic Claude client implementation"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = anthropic.Anthropic(
            api_key=api_key or current_app.config['ANTHROPIC_API_KEY']
        )
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        context: Optional[str] = None,
        stream: bool = False
    ) -> Union[str, AsyncGenerator[str, None]]:
        # Convert messages to Claude format
        prompt = self._format_messages(messages, context)
        
        if stream:
            return self._stream_completion(prompt)
        else:
            return self._complete(prompt)
    
    def _format_messages(self, messages: List[Dict[str, str]], context: Optional[str] = None) -> str:
        """Format messages into Claude prompt format"""
        formatted = []
        
        if context:
            formatted.append(f"Context:\n{context}\n\nConversation:")
            
        for msg in messages:
            role = "Human" if msg['role'] == 'user' else "Assistant"
            formatted.append(f"{role}: {msg['content']}")
            
        return "\n\n".join(formatted)
    
    def _complete(self, prompt: str) -> str:
        """Generate a complete response"""
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    async def _stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream the response"""
        stream = self.client.messages.stream(
            model="claude-3-sonnet-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        async for chunk in stream:
            if chunk.type == "content_block_delta":
                yield chunk.delta.text 