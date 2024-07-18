import hashlib
from typing import Optional

from resources.objects import User


def get_user_from_email(email: str) -> Optional[User]:
    user = User.get_instance_where(where_clause=f"user_email = '{email}'")
    if user.user_email == email:
        return user
    return None


def get_user_from_id(user_id: str) -> User:
    return User.get_instance(id=user_id)


def add_user(email: str, password: str, first_name: str, last_name: str) -> User:
    if get_user_from_email(email=email):
        raise ValueError(f"User with {email} already exists")
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    return User.create_instance(
        {
            "user_email": email,
            "password": hash_pass,
            "first_name": first_name,
            "last_name": last_name,
            "is_email_verified": False,
        }
    )
