from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_bootstrap import Bootstrap
from src.auth import auth_user, register_user, register_symptom, get_symptoms
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/success')
def success():
    if not session.get('logged_in'):
        return redirect('/')

    return render_template('dashboard.html', username=session['username'])


@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if request.method == 'GET':
        with open('symptom_data.json', 'r') as f:
            symptom_data = json.load(f)
        symptoms = []
        for category in symptom_data:
            for symptom in symptom_data[category]:
                symptoms.append(symptom.lower())
        symptoms.sort()
        return render_template('tracker.html', symptoms=symptoms)
    elif request.method == 'POST':
        symptom = request.form['symptoms']
        date = request.form['date']
        time = request.form['time']

        if not session.get('logged_in'):
            return redirect('/error')

        username = session['username']
        success = register_symptom(username, symptom, date, time)
        if not success:
            return redirect('/error')
        return redirect('/success')



@app.route('/log')
def log():
    if not session.get('logged_in'):
        return redirect('/error')
    username = session['username']
    symptoms = get_symptoms(username)
    return render_template('log.html', symptoms=symptoms)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = auth_user(username, password)
        if user:
            session['username'] = user.username
            session['logged_in'] = True
            return redirect('/success')
        else:
            flash('Invalid username or password')
            return redirect('/login')
    else:
        return redirect('/error')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        user = register_user(username, password, email)

        if user:
            flash('Success! Account created.')
            return redirect('/')
        else:
            flash('Username taken! Please choose another username')
            return redirect('/register')
    else:
        return redirect('/error')


@app.route('/error')
def error():
    return 'error'


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'this_is_totally_a_secret'
    bootstrap = Bootstrap(app)
    app.run(debug=True)
