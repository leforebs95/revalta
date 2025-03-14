import requests
from typing import Dict, List, Optional, Union
from uuid import UUID
from http import HTTPStatus
from contextlib import contextmanager

class VectorClient:
    """Client for interacting with the Vector API service."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        """Initialize the Vector API client.
        
        Args:
            base_url: Base URL of the Vector API service
        """
        self.base_url = base_url.rstrip('/')
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
        # Temporarily set user_id for this operation
        previous_user_id = self._user_id
        self._user_id = user_id
        
        try:
            payload = {
                "userId": self._user_id,
                "text": text
            }
            
            response = requests.post(
                f"{self.base_url}/api/vector/document",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        finally:
            # Restore previous user_id
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
    
    def keyword_search(
        self,
        user_id: Optional[int] = None,
        keyword: str = None,
        k: int = 5
    ) -> Dict[str, List]:
        """Perform keyword search.
        
        Args:
            user_id: Optional ID of the user. If not provided, uses current user_id
            keyword: Keyword to search for
            k: Number of results to return
            
        Returns:
            Dict containing search results
        """
        # Use provided user_id or current one
        effective_user_id = user_id if user_id is not None else self._user_id
        if effective_user_id is None:
            raise ValueError("No user_id provided or set in client")
            
        payload = {
            "userId": effective_user_id,
            "keyword": keyword,
            "k": k
        }
        
        response = requests.post(
            f"{self.base_url}/api/vector/search/keyword",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def get_document(
        self, 
        document_id: Union[str, UUID], 
        user_id: Optional[int] = None
    ) -> Dict:
        """Retrieve a document by its ID.
        
        Args:
            document_id: UUID of the document to retrieve
            user_id: Optional ID of the user. If not provided, uses current user_id
            
        Returns:
            Dict containing document information
        """
        # Use provided user_id or current one
        effective_user_id = user_id if user_id is not None else self._user_id
        if effective_user_id is None:
            raise ValueError("No user_id provided or set in client")
            
        response = requests.get(
            f"{self.base_url}/api/vector/document/{document_id}",
            params={"userId": effective_user_id}
        )
        response.raise_for_status()
        return response.json() 