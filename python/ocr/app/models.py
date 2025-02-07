from datetime import datetime, timezone
from typing import Optional
import uuid
from sqlalchemy import String, DateTime, Boolean, Text, JSON, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

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


class DocumentPage(BaseModel):
    """Stores OCR results for individual document pages."""

    __tablename__ = "document_pages"

    page_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    page_path: Mapped[str] = mapped_column(String(255), nullable=False)
    text_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    last_attempt: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", index=True)

    def to_dict(self):
        return {
            "page_id": str(self.page_id),
            "file_id": self.file_id,
            "page_number": self.page_number,
            "page_path": self.page_path,
            "text_content": self.text_content,
            "raw_data": self.raw_data,
            "confidence": self.confidence,
            "retry_count": self.retry_count,
            "last_attempt": (
                self.last_attempt.isoformat() if self.last_attempt else None
            ),
            "error_message": self.error_message,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
