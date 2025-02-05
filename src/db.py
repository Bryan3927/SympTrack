import sqlite3
db = 'symptrack.db'


def create_tables():
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS auth_table ('''
              '''username message_text, '''
              '''password message_text, '''
              '''email message_text);''')

    c.execute('''CREATE TABLE IF NOT EXISTS symptom_table ('''
              '''username message_text, '''
              '''symptom message_text, '''
              '''date date,'''
              '''time time,'''
              '''severity integer,'''
              '''notes message_text);''')

    conn.commit()
    conn.close()


def verify_user(username, password):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    user = c.execute('''SELECT * FROM auth_table WHERE username=? AND password=?;''',
                     (username, password)).fetchone()
    conn.commit()
    conn.close()

    if user:
        return user
    return False


def create_user(username, password, email):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    user = c.execute('''SELECT * FROM auth_table WHERE username=?;''',
                     (username,)).fetchone()
    if not user:
        c.execute('''INSERT into auth_table VALUES (?,?,?);''',
                  (username, password, email))

    conn.commit()
    conn.close()

    if not user:
        return True
    return False


def add_symptom(username, symptom, datetime, severity, notes):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''INSERT into symptom_table VALUES (?,?,?,?,?);''',
              (username, symptom, datetime, severity, notes))

    conn.commit()
    conn.close()

    return True


def find_symptoms(username):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    symptoms = c.execute('''SELECT * FROM symptom_table WHERE username=?;''',
                         (username, )).fetchall()

    conn.commit()
    conn.close()

    return symptoms


def find_data_for_symptom(username, symptom):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    symptoms = c.execute('''SELECT * FROM symptom_table WHERE username=? AND symptom=?;''',
                         (username, symptom)).fetchall()

    conn.commit()
    conn.close()

    return symptoms

def delete_all_user_symptoms(username):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    c.execute('''DELETE FROM symptom_table WHERE username=?''', (username,))

    conn.commit()
    conn.close()

    return True

if __name__ == '__main__':
    create_tables()
