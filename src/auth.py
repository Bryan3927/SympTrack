from .user import User
from .db import verify_user, create_user, add_symptom, find_symptoms


def auth_user(username, password):
    user = verify_user(username, password)
    if not user:
        return None
    return User(user[0])


def register_user(username, password, email):
    return create_user(username, password, email)
