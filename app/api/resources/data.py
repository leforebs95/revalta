import hashlib

from resources.objects import Book
from resources.objects import User


def get_book_from_title(title: str):
    return Book.get_instance_where(where_clause=f"title = '{title}'")


def get_user_from_username(username: str):
    user = User.get_instance_where(where_clause=f"username = '{username}'")
    if user.username == username:
        return user
    return None


def get_user_from_email(email: str):
    user = User.get_instance_where(where_clause=f"user_email = '{email}'")
    if user.user_email == email:
        return user
    return None


def get_user_from_id(user_id: str):
    return User.get_instance(id=user_id)


def add_user(username: str, password: str, email: str):
    if get_user_from_username(username=username):
        raise ValueError(f"User with {username} already exists")
    if get_user_from_email(email=email):
        raise ValueError(f"User with {email} already exists")
    hash_pass = hashlib.sha256(password.encode()).hexdigest()
    return User.create_instance(
        {
            "username": username,
            "password": hash_pass,
            "user_email": email,
            "is_email_verified": False,
        }
    )
