from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean, BigInteger
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


class File(BaseModel):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)

    def to_json(self):
        return {
            "fileId": self.file_id,
            "userId": self.user_id,
            "filename": self.filename,
            "originalFilename": self.original_filename,
            "fileSize": self.file_size,
            "mimeType": self.mime_type,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }
