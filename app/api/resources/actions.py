import hashlib
from typing import Optional

from resources.objects import User


def get_user_from_email(user_email: str) -> Optional[User]:
    print(f"Fetching user with email: {user_email}")
    user = User.get_instance_where(where_clause=f"user_email = '{user_email}'")
    if user.user_email == user_email:
        return user
    return None


def get_user_from_id(user_id: str) -> User:
    return User.get_instance(id=user_id)


def add_user(email: str, password: str, first_name: str, last_name: str) -> User:
    if user := get_user_from_email(user_email=email):
        print(user)
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
