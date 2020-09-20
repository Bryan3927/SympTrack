from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_bootstrap import Bootstrap
from src.auth import auth_user, register_user


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/success')
def success():
    if not session.get('logged_in'):
        return redirect('/')

    return render_template('dashboard.html', username=session['username'])


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
