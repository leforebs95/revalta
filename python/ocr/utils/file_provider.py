from abc import ABC, abstractmethod
from typing import BinaryIO
from urllib import request
import requests
from io import BytesIO
import uuid


class FileProvider(ABC):
    """Interface for retrieving files from different sources"""

    @abstractmethod
    def get_file(self, file_id: uuid.UUID) -> BinaryIO:
        """Get file as binary stream from source

        Args:
            file_id: UUID of file to retrieve

        Returns:
            Binary file stream
        """
        pass


class UploadServiceProvider(FileProvider):
    """Gets files from upload service"""

    def __init__(self, upload_service_url: str):
        self.url = upload_service_url

    def get_file(self, file_id: uuid.UUID) -> BinaryIO:
        try:
            response = requests.get(f"{self.url}/{file_id}/download")
            if response.status_code == 200:
                return BytesIO(response.content)
            else:
                raise Exception(
                    f"Failed to get file. Status code: {response.status_code}"
                )
        except Exception as e:
            raise Exception(f"Error getting file: {str(e)}")


class S3Provider(FileProvider):
    """Gets files from S3"""

    def __init__(self, bucket: str, region: str = "us-west-2"):
        self.bucket = bucket
        self.region = region

    def get_file(self, file_id: uuid.UUID) -> BinaryIO:
        # Implementation to get file from S3
        pass
