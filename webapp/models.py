from flask_login import UserMixin

from . import db, login_manager


def get_user(username):
    c = db.cursor(named_tuple=True)
    c.execute("SELECT * FROM Users WHERE username=%s;",
              (username,))
    user = c.fetchone()

    return user


@login_manager.user_loader
def load_user(user_id):
    u = get_user(user_id)
    return User(u.username) if u else None


class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username
