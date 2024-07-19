from flask_login import UserMixin


class UserSession(UserMixin):

    def __init__(self, user_id: str):
        self.user_id = user_id

    def get_id(self):
        return self.user_id
