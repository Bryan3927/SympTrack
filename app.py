from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from src.auth import auth_user, register_user
from src.track import register_symptom, get_symptoms, delete_user_data
from src.analytics import build_figure
import json


app = Flask(__name__)


def list_symptoms():
    with open('symptom_data.json', 'r') as f:
        symptom_data = json.load(f)
    symptoms = []
    for category in symptom_data:
        for symptom in symptom_data[category]:
            symptoms.append(symptom.lower())
    symptoms.sort()
    return symptoms


@app.route('/')
def hello_world():
    if session.get('logged_in'):
        return redirect('/dashboard')
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/')

    return render_template('dashboard.html', username=session['username'])


@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    if request.method == 'GET':
        symptoms = list_symptoms()
        return render_template('tracker.html', symptoms=symptoms)
    elif request.method == 'POST':
        symptom = request.form['symptoms']
        datetime = request.form['datetime']
        severity = request.form['severity']
        notes = request.form['notes']

        if not session.get('logged_in'):
            return redirect('/error')

        username = session['username']
        success = register_symptom(username, symptom, datetime, severity, notes)
        if not success:
            return redirect('/error')
        return redirect('/dashboard')


@app.route('/log')
def log():
    if not session.get('logged_in'):
        return redirect('/error')
    username = session['username']
    symptoms = get_symptoms(username)

    return render_template('log.html', symptoms=symptoms)

@app.route('/deleted', methods=['POST'])
def deleted():
    if not session.get('logged_in'):
        return redirect('/error')
    if request.method == 'POST':
        username = session['username']
        success = delete_user_data(username)
        if not success:
            return redirect('/error')
        return redirect('/log')

@app.route('/analytics', methods=['GET', 'POST'])
def analytics():
    if not session.get('logged_in'):
        return redirect('/error')

    if request.method == 'GET':
        symptoms = list_symptoms()
        return render_template('analytics.html', symptoms=symptoms)

    elif request.method == 'POST':
        symptom = request.form['symptoms']
        return redirect(f'/analytics/{symptom}')


@app.route('/analytics/<symptom>')
def advanced_analytics(symptom):
    if not session.get('logged_in'):
        return redirect('/error')
    username = session['username']
    filename = build_figure(username, symptom)

    return render_template('advanced_analytics.html', symptom=symptom, filename=filename)


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
            return redirect('/dashboard')
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


@app.route('/logout')
def logout():
    if session.get('logged_in'):
        session['logged_in'] = False
    return redirect('/')


@app.route('/error')
def error():
    return 'error'


# disable cache
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'this_is_totally_a_secret'
    bootstrap = Bootstrap(app)
    app.run(debug=True)
