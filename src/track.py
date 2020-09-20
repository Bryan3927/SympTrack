from .db import verify_user, create_user, add_symptom, find_symptoms


def register_symptom(username, symptom, date, time, notes):
    return add_symptom(username, symptom, date, time, notes)


def get_symptoms(username):
    return find_symptoms(username)
