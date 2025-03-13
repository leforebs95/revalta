# llm_clients/anthropic.py
import os
from pathlib import Path
import anthropic
from typing import Dict, Any, Optional, List
from .base import BaseLLMClient


class AnthropicClient(BaseLLMClient):
    """Client for Anthropic's API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-opus-20240229",
        system: Optional[str] = None,
        system_prompt_path: Optional[
            str
        ] = "./utils/llm_clients/prompts/ocr_prompt.txt",
    ):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable"
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model

        # Handle system prompt from file if path is provided
        if system_prompt_path:
            self.system = self._load_system_prompt(system_prompt_path)
        else:
            self.system = system

    def _load_system_prompt(self, filepath: str) -> str:
        """Load system prompt from a text file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"System prompt file not found: {filepath}")

        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def generate(
        self,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        system_prompt_path: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Generate a response from Claude based on the prompt."""
        # Determine which system prompt to use, with priority:
        # 1. Directly provided system prompt
        # 2. System prompt from file path
        # 3. System prompt from initialization
        if system:
            system_message = system
        elif system_prompt_path:
            system_message = self._load_system_prompt(system_prompt_path)
        else:
            system_message = self.system

        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
            **kwargs,
        }

        if system_message:
            params["system"] = system_message

        response = self.client.messages.create(**params)
        return response.content[0].text

    def generate_with_context(
        self,
        prompt: str,
        context: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system: Optional[str] = None,
        system_prompt_path: Optional[str] = None,
        **kwargs,
    ) -> str:
        """Generate a response using additional context messages."""
        # Determine which system prompt to use with same priority as generate method
        if system:
            system_message = system
        elif system_prompt_path:
            system_message = self._load_system_prompt(system_prompt_path)
        else:
            system_message = self.system

        messages = context + [{"role": "user", "content": prompt}]

        params = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            **kwargs,
        }

        if system_message:
            params["system"] = system_message

        response = self.client.messages.create(**params)
        return response.content[0].text
