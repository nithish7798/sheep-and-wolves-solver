from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import User, GameSession
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password matches
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Successful login
            flash('Login successful!', 'success')
            return redirect(url_for('play_game'))
        else:
            # Invalid credentials
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login'))

    # Handle GET request to display login form
    return render_template('login.html', title='Sign In')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username is already taken. Please choose a different one.', 'error')
            return redirect(url_for('signup'))

        # If username is available, create a new user and add to the database
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Sign up successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    # Handle GET request to display signup form
    return render_template('signup.html', title='Sign Up')

@app.route('/play_game')
def play_game():
    return render_template('play_game.html', title='Play Game')
@app.route('/logout')
def logout():
    # Perform logout logic here (e.g., clear session, redirect to login page)
    # For example:
    # session.clear()  # Clear session data if using Flask session
    return redirect(url_for('login'))  # Redirect to the login page
