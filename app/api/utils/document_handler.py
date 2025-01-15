# app/api/document_handler/document_handler.py
from models import Document
import mimetypes
import hashlib
from pathlib import Path
import boto3


class DocumentHandler:
    def __init__(self, db):
        self.s3_client = boto3.client("s3")
        self.db = db
        self.bucket_name = "nivalta-health"

    def _get_mime_type(self, filename: str) -> str:
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            raise ValueError(f"Unable to determine MIME type for {filename}")
        return mime_type

    def _generate_s3_key(self, user_id: int, file_hash: str, filename: str) -> str:
        extension = Path(filename).suffix
        return f"users/{user_id}/documents/{file_hash}{extension}"

    def process_document(
        self, s3_key: str, filename: str, mime_type: str, user_id: int
    ) -> Document:
        document = Document(
            title=Path(filename).stem,
            original_filename=filename,
            mime_type=mime_type,
            s3_location=s3_key,
            user_id=user_id,
        )

        self.db.session.add(document)
        self.db.session.commit()
        return document
