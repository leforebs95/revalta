from flask_login import UserMixin

from resources.objects import User


class UserSession(UserMixin):

    def __init__(self, user_id: str):
        self.user_id = user_id
