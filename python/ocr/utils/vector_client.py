import requests
from typing import Dict, List, Optional, Union
from uuid import UUID
from http import HTTPStatus

class VectorClient:
    """Client for interacting with the Vector API service."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize the Vector API client.
        
        Args:
            base_url: Base URL of the Vector API service
        """
        self.base_url = base_url.rstrip('/')
        
    def get_version(self) -> Dict[str, str]:
        """Get the API version.
        
        Returns:
            Dict containing version information
        """
        response = requests.get(f"{self.base_url}/api/vector/version")
        response.raise_for_status()
        return response.json()
    
    def insert_document(self, user_id: int, text: str) -> Dict[str, Union[str, int]]:
        """Insert a document into the vector database.
        
        Args:
            user_id: ID of the user
            text: Document text to insert
            
        Returns:
            Dict containing document ID and number of chunks
        """
        payload = {
            "userId": user_id,
            "text": text
        }
        
        response = requests.post(
            f"{self.base_url}/api/vector/document",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
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
    
    def keyword_search(
        self,
        user_id: int,
        keyword: str,
        k: int = 5
    ) -> Dict[str, List]:
        """Perform keyword search.
        
        Args:
            user_id: ID of the user
            keyword: Keyword to search for
            k: Number of results to return
            
        Returns:
            Dict containing search results
        """
        payload = {
            "userId": user_id,
            "keyword": keyword,
            "k": k
        }
        
        response = requests.post(
            f"{self.base_url}/api/vector/search/keyword",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_document(self, document_id: Union[str, UUID], user_id: int) -> Dict:
        """Retrieve a document by its ID.
        
        Args:
            document_id: UUID of the document to retrieve
            user_id: ID of the user
            
        Returns:
            Dict containing document information
        """
        response = requests.get(
            f"{self.base_url}/api/vector/document/{document_id}",
            params={"userId": user_id}
        )
        response.raise_for_status()
        return response.json() 