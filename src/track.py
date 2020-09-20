from .db import add_symptom, find_symptoms


def register_symptom(username, symptom, date, time, severity, notes):
    return add_symptom(username, symptom, date, time, severity, notes)


def get_symptoms(username):
    return find_symptoms(username)
