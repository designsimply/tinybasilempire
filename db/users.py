from flask_login import UserMixin

from db import query_db


class User(UserMixin):
    """Database User.

    This User represents the database users table. Attributes should map 1:1.

    id, name, email, profile_pic

    """

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get_from_email(user_email):
        users = query_db(
            "SELECT id, name, email, profile_pic FROM basil_users WHERE email=%s",
            params=(user_email,),
        )
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise RuntimeError(f"Too many users! {users}")
        else:
            user = users[0]
            return User(
                id_=user.id,
                name=user.name,
                email=user.email,
                profile_pic=user.profile_pic,
            )

    @staticmethod
    def get(user_id):
        users = query_db("select * from basil_users where id=%s", params=(user_id,))
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise RuntimeError(f"Too many users! {users}")
        else:
            user = users[0]
            return User(
                id_=user.id,
                name=user.name,
                email=user.email,
                profile_pic=user.profile_pic,
            )

    @staticmethod
    def update(name, email, profile_pic):
        users = query_db(
            "UPDATE basil_users "
            "SET name=%(name)s, email=%(email)s, profile_pic=%(profile_pic)s "
            "WHERE email = %(email)s"
            "RETURNING * ",
            params={
                "name": name,
                "email": email,
                "profile_pic": profile_pic,
            },
        )
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise RuntimeError(f"Too many users! {users}")
        else:
            user = users[0]
            return User(
                id_=user.id,
                name=user.name,
                email=user.email,
                profile_pic=user.profile_pic,
            )

    @staticmethod
    def create(name, email, profile_pic):
        users = query_db(
            "INSERT INTO basil_users (name, email, profile_pic) "
            "VALUES (%s, %s, %s) "
            "RETURNING * ",
            (name, email, profile_pic),
        )
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise RuntimeError(f"Too many users! {users}")
        else:
            user = users[0]
            return User(
                id_=user.id,
                name=user.name,
                email=user.email,
                profile_pic=user.profile_pic,
            )
