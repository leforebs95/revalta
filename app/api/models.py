from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from flask_app import db
from flask_login import UserMixin


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


class Waitlist(BaseModel):
    __tablename__ = "waitlist"

    email: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return super().__repr__()

    def to_json(self):
        return {
            "email": self.email,
            "name": self.name,
            "message": self.message,
        }


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


class Symptom(BaseModel):
    __tablename__ = "symptoms"

    symptom_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symptom_name: Mapped[str] = mapped_column(String(50), nullable=False)
    symptom_description: Mapped[str] = mapped_column(String(255), nullable=False)
    symptom_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", backref=db.backref("symptoms", order_by=symptom_id))

    def __repr__(self) -> str:
        return super().__repr__()

    def to_json(self):
        return {
            "symptomId": self.symptom_id,
            "symptomName": self.symptom_name,
            "symptomDescription": self.symptom_description,
            "symptomDuration": self.symptom_duration,
        }


class LabResult(BaseModel):
    __tablename__ = "lab_results"

    result_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_location: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.user_id"))

    user = db.relationship(
        "User", backref=db.backref("lab_results", order_by=result_id)
    )

    def __repr__(self) -> str:
        return super().__repr__()

    def to_json(self):
        return {
            "resultId": self.result_id,
            "name": self.name,
            "description": self.description,
            "s3Location": self.s3_location,
        }
