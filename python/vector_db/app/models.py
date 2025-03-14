from datetime import datetime, timezone
import uuid
from sqlalchemy import Text, String, Integer, BigInteger, DateTime, Boolean, ForeignKey, Index, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
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

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    chunks = relationship("DocumentChunk", back_populates="document", passive_deletes=True)

    __table_args__ = (
        Index('idx_documents_user_id', 'user_id'),
        CheckConstraint('user_id > 0', name='check_valid_user_id_doc'),
    )


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    chunk_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.document_id", ondelete='CASCADE'),
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    document = relationship("Document", back_populates="chunks")
    chunk_seq_number: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list] = mapped_column(Vector(384))
    chunk_metadata: Mapped[dict] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index('idx_chunks_user_id', 'user_id'),
        Index('idx_chunks_document_user', 'document_id', 'user_id'),
        ForeignKeyConstraint(
            ['document_id', 'user_id'],
            ['documents.document_id', 'documents.user_id'],
            name='fk_chunk_document_user'
        ),
        CheckConstraint('user_id > 0', name='check_valid_user_id_chunk'),
    )
