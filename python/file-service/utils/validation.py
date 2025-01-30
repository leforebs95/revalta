import os
from typing import Optional
from werkzeug.datastructures import FileStorage


def validate_file(
    file: FileStorage, max_size_bytes: int = 536_870_912
) -> tuple[bool, Optional[str]]:
    """
    Validate uploaded file.

    Args:
        file: The uploaded file
        max_size_bytes: Maximum allowed file size in bytes (default: 512MB)

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"

    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer

    if size > max_size_bytes:
        return (
            False,
            f"File size exceeds maximum allowed size of {max_size_bytes/1024/1024:.0f}MB",
        )

    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        return False, "Only PDF files are allowed"

    return True, None
