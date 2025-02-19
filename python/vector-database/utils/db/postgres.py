from typing import List, Dict, Optional
import uuid
from sqlalchemy import text
from app.models import db, Document, DocumentChunk
from .base import BaseVectorDB


class PostgresVectorDB(BaseVectorDB):
    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.schema_name = f"user_{user_id}"

    def initialize_user_schema(self):
        with db.session.connection() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

        Document.__table__.schema = self.schema_name
        DocumentChunk.__table__.schema = self.schema_name
        db.create_all()

    def insert_document(self, text: str, chunks: List[Dict]) -> uuid.UUID:
        try:
            doc = Document(user_id=self.user_id)
            db.session.add(doc)
            db.session.flush()

            for chunk_data in chunks:
                chunk = DocumentChunk(
                    document_id=doc.document_id,
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
        query = db.session.query(DocumentChunk)
        if score_threshold:
            query = query.filter(
                DocumentChunk.embedding.cosine_distance(query_embedding)
                <= score_threshold
            )

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
        results = (
            db.session.query(DocumentChunk)
            .filter(DocumentChunk.chunk_text.ilike(f"%{keyword}%"))
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
        doc = (
            db.session.query(Document)
            .filter(Document.document_id == document_id)
            .first()
        )

        if not doc:
            return None

        chunks = (
            db.session.query(DocumentChunk)
            .filter(DocumentChunk.document_id == document_id)
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
