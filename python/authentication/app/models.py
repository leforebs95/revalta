from datetime import datetime, timezone
from typing import Dict
from sqlalchemy import JSON, Integer, String, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    _user_email: Mapped[str] = mapped_column(
        "user_email", String(50), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @hybrid_property
    def user_email(self):
        return self._user_email

    @user_email.setter
    def user_email(self, email):
        self._user_email = email.lower()

    def to_json(self):
        return {
            "userId": self.user_id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "userEmail": self.user_email,
            "isEmailVerified": self.is_email_verified,
            "createdAt": self.created_at,
            "lastLogin": self.last_login,
        }

    def get_id(self):
        return self.user_id
