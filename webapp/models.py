from flask_login import UserMixin

from . import db, login_manager


def get_user(username):
    c = db.cursor(named_tuple=True)
    c.execute(
        "SELECT Users.*, Students.univid, Students.email FROM Users "
        "LEFT JOIN Students ON Users.username = Students.username "
        "WHERE Users.username = %s",
        (username,))
    user = c.fetchone()

    return user


@login_manager.user_loader
def load_user(user_id):
    u = get_user(user_id)
    return User(u) if u else None


class User(UserMixin):
    def __init__(self, row):
        self.username = row.username
        self.univid = row.univid
        self.email = row.email

    def get_id(self):
        return self.username
