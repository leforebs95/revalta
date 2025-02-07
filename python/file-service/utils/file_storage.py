import json
import os
import logging
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional
import redis
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)


class FileStorage(ABC):
    """Abstract base class for file storage implementations."""

    @abstractmethod
    def save_file(
        self, file: BinaryIO, filename: str
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """Save a file to storage."""
        pass

    @abstractmethod
    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        """Retrieve a file from storage."""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage."""
        pass


class LocalFileStorage(FileStorage):
    """Local filesystem storage implementation."""

    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename while preserving the original extension."""
        ext = os.path.splitext(original_filename)[1]
        return f"{uuid.uuid4()}{ext}"

    def save_file(
        self, file: BinaryIO, filename: str
    ) -> tuple[bool, Optional[str], Optional[str]]:
        """
        Save a file to local storage.

        Args:
            file: File-like object to save
            filename: Original filename

        Returns:
            Tuple of (success, stored_filename, file_path)
        """
        try:
            secure_fname = secure_filename(filename)
            if not secure_fname:
                logger.error("Invalid filename")
                return False, None, None

            unique_filename = self._generate_unique_filename(secure_fname)
            file_path = os.path.join(self.upload_dir, unique_filename)

            # Ensure upload directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Save file
            file.save(file_path)

            logger.info(f"Saved file {unique_filename}")
            return True, unique_filename, file_path

        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            return False, None, None

    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        """
        Retrieve a file from local storage.

        Args:
            file_path: Path to the file

        Returns:
            File object if found, None otherwise
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None

            return open(file_path, "rb")

        except Exception as e:
            logger.error(f"Error retrieving file: {str(e)}")
            return None

    def delete_file(self, file_path: str) -> bool:
        """
        Delete a file from local storage.

        Args:
            file_path: Path to the file

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return False

            os.remove(file_path)
            logger.info(f"Deleted file: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
