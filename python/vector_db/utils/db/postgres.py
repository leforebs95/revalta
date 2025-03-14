from typing import List, Dict, Optional
import uuid
from sqlalchemy import text
from app.models import db, Document, DocumentChunk
from .base import BaseVectorDB


class PostgresVectorDB(BaseVectorDB):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def initialize_user_schema(self):
        """
        Initialize vector extension if not already done.
        No longer needs to create per-user schema.
        """
        with db.session.connection() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

    def insert_document(self, text: str, chunks: List[Dict]) -> uuid.UUID:
        try:
            # Create document with user_id
            doc = Document(user_id=self.user_id)
            db.session.add(doc)
            db.session.flush()  # Get the document_id

            # Create chunks with same user_id
            for chunk_data in chunks:
                chunk = DocumentChunk(
                    document_id=doc.document_id,
                    user_id=self.user_id,  # Important: Set user_id on chunk
                    chunk_seq_number=chunk_data["seq_number"],
                    chunk_text=chunk_data["text"],
                    embedding=chunk_data["embedding"],
                    chunk_metadata=chunk_data.get("metadata", {}),
                )
                db.session.add(chunk)

            db.session.commit()
            return doc.document_id

        except Exception as e:
            db.session.rollback()
            raise e

    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        score_threshold: Optional[float] = None,
    ) -> List[Dict]:
        # Base query with user filtering
        query = db.session.query(DocumentChunk).filter(
            DocumentChunk.user_id == self.user_id,
            DocumentChunk.is_deleted == False
        )

        # Add score threshold if specified
        if score_threshold:
            query = query.filter(
                DocumentChunk.embedding.cosine_distance(query_embedding)
                <= score_threshold
            )

        # Get results
        results = (
            query.order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(k)
            .all()
        )

        return [
            {
                "chunk_id": str(r.chunk_id),
                "document_id": str(r.document_id),
                "text": r.chunk_text,
                "metadata": r.chunk_metadata,
                "score": r.embedding.cosine_distance(query_embedding),
            }
            for r in results
        ]

    def keyword_search(self, keyword: str, k: int = 5) -> List[Dict]:
        # Query with user filtering
        results = (
            db.session.query(DocumentChunk)
            .filter(
                DocumentChunk.user_id == self.user_id,
                DocumentChunk.is_deleted == False,
                DocumentChunk.chunk_text.ilike(f"%{keyword}%")
            )
            .limit(k)
            .all()
        )

        return [
            {
                "chunk_id": str(r.chunk_id),
                "document_id": str(r.document_id),
                "text": r.chunk_text,
                "metadata": r.chunk_metadata,
            }
            for r in results
        ]

    def get_document(self, document_id: uuid.UUID) -> Optional[Dict]:
        # Query document with user filtering
        doc = (
            db.session.query(Document)
            .filter(
                Document.document_id == document_id,
                Document.user_id == self.user_id,
                Document.is_deleted == False
            )
            .first()
        )

        if not doc:
            return None

        # Query chunks with user filtering (though document filter should be sufficient)
        chunks = (
            db.session.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id,
                DocumentChunk.user_id == self.user_id,
                DocumentChunk.is_deleted == False
            )
            .order_by(DocumentChunk.chunk_seq_number)
            .all()
        )

        return {
            "document_id": str(doc.document_id),
            "chunks": [
                {
                    "chunk_id": str(c.chunk_id),
                    "text": c.chunk_text,
                    "seq_number": c.chunk_seq_number,
                    "metadata": c.chunk_metadata,
                }
                for c in chunks
            ],
        }
