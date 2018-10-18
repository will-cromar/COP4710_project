from flask_login import UserMixin

from . import db, login_manager


def get_user(username):
    c = db.cursor(named_tuple=True)
    c.execute(
        "SELECT * FROM EasyUsers "
        "WHERE username = %s",
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
        self.super = row.super

    def get_id(self):
        return self.username

    def is_student(self):
        return self.univid is not None

    def is_super_user(self):
        return self.super

    def get_rsos(self):
        c = db.cursor()
        c.execute(
            "SELECT RSOs.rid, rsoname "
            "FROM RSOs "
            "JOIN RSOMembers ON RSOs.rid = RSOMembers.rid "
            "WHERE RSOMembers.username = %s",
            (self.username,))

        return c.fetchall()
