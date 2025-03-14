import requests
from typing import Dict, List, Optional, Union
from uuid import UUID
from http import HTTPStatus
from flask import current_app

class VectorClient:
    """Client for interacting with the Vector API service."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the Vector API client.
        
        Args:
            base_url: Base URL of the Vector API service
        """
        self.base_url = (base_url or current_app.config['VECTOR_API_URL']).rstrip('/')
    
    def similarity_search(
        self,
        user_id: int,
        query_text: str,
        k: int = 5,
        score_threshold: Optional[float] = None
    ) -> Dict[str, List]:
        """Perform similarity search.
        
        Args:
            user_id: ID of the user
            query_text: Text to search for
            k: Number of results to return
            score_threshold: Optional minimum similarity score threshold
            
        Returns:
            Dict containing search results
        """
        payload = {
            "userId": user_id,
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