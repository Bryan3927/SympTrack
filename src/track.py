from .db import add_symptom, find_symptoms, delete_all_user_symptoms


def register_symptom(username, symptom, datetime, severity, notes):
    return add_symptom(username, symptom, datetime, severity, notes)


def get_symptoms(username):
    return find_symptoms(username)

def delete_user_data(username):
    return delete_all_user_symptoms(username)
