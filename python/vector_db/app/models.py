from datetime import datetime, timezone
import uuid
from sqlalchemy import Text, String, Integer, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, VECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def soft_delete(self):
        self.is_deleted = True
        self.updated_at = datetime.now(timezone.utc)


class Document(BaseModel):
    __tablename__ = "documents"
    __table_args__ = {"schema": "user_schema"}  # Dynamic schema per user

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    chunks = relationship("DocumentChunk", back_populates="document")


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"
    __table_args__ = {"schema": "user_schema"}  # Dynamic schema per user

    chunk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_schema.documents.document_id"),
        nullable=False,
    )
    document = relationship("Document", back_populates="chunks")
    chunk_seq_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list] = mapped_column(
        VECTOR(384)
    )  # Default dimension, configurable
    chunk_metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
