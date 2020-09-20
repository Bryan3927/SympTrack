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
              '''time time);''')

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


def add_symptom(username, symptom, date, time):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    c.execute('''INSERT into symptom_table VALUES (?,?,?,?);''',
              (username, symptom, date, time))

    conn.commit()
    conn.close()

    return True


def find_symptoms(username):
    conn = sqlite3.connect(db)
    c = conn.cursor()

    symptoms = c.execute('''SELECT * FROM symptom_table WHERE username=?;''',
                         (username,)).fetchall()

    conn.commit()
    conn.close()

    return symptoms


if __name__ == '__main__':
    create_tables()
