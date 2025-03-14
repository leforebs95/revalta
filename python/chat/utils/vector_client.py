import requests
from typing import Dict, List, Optional, Union
from uuid import UUID
from http import HTTPStatus
from flask import current_app
from contextlib import contextmanager

class VectorClient:
    """Client for interacting with the Vector API service."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the Vector API client.
        
        Args:
            base_url: Base URL of the Vector API service
        """
        self.base_url = (base_url or current_app.config['VECTOR_API_URL']).rstrip('/')
        self._user_id = None
        
    @property
    def user_id(self) -> Optional[int]:
        """Get current user ID."""
        return self._user_id
        
    @user_id.setter
    def user_id(self, value: Optional[int]):
        """Set current user ID."""
        self._user_id = value
        
    @contextmanager
    def system_context(self):
        """Context manager for system-level operations.
        
        Usage:
            with vector_client.system_context():
                # Operations here run with system privileges
        """
        previous_user_id = self._user_id
        try:
            self._user_id = None
            yield
        finally:
            self._user_id = previous_user_id
    
    def similarity_search(
        self,
        user_id: Optional[int] = None,
        query_text: str = None,
        k: int = 5,
        score_threshold: Optional[float] = None
    ) -> Dict[str, List]:
        """Perform similarity search.
        
        Args:
            user_id: Optional ID of the user. If not provided, uses current user_id
            query_text: Text to search for
            k: Number of results to return
            score_threshold: Optional minimum similarity score threshold
            
        Returns:
            Dict containing search results
        """
        # Use provided user_id or current one
        effective_user_id = user_id if user_id is not None else self._user_id
        if effective_user_id is None:
            raise ValueError("No user_id provided or set in client")
            
        payload = {
            "userId": effective_user_id,
            "queryText": query_text,
            "k": k
        }
        
        if score_threshold is not None:
            payload["scoreThreshold"] = score_threshold
            
        response = requests.post(
            f"{self.base_url}/api/vector/search/similarity",
            json=payload
        )
        response.raise_for_status()
        return response.json() 