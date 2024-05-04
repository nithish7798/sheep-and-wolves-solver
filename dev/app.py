from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from collections import deque
from semanticnetsagent import SemanticNetsAgent, State
from solution import bfs_solution  # Ensure this is imported correctly at the top

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), default='')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}')"

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/solution', methods=['POST'])
def solution():
    try:
        initialSheep = int(request.form['initialSheep'])
        initialWolves = int(request.form['initialWolves'])
    except ValueError:
        return jsonify({'error': 'Invalid input data: Non-integer values provided'}), 400
    except KeyError:
        return jsonify({'error': 'Invalid input data: Missing fields'}), 400

    solution_steps = bfs_solution(initialSheep, initialWolves)
    if solution_steps is None:
        solution_steps = ["No valid solution exists for the given number of sheep and wolves."]
    elif not solution_steps:
        solution_steps = ["No possible solution could be found."]
    else:
        solution_steps = [str(step) for step in solution_steps]  # Ensure steps are strings

    return render_template('solution.html', steps=solution_steps)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        
        try:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                error = 'Email already exists. Please use a different email or login to continue.'
                return render_template('signup.html', error=error)

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(fullname=fullname, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except (IntegrityError, OperationalError) as e:
            db.session.rollback()
            error = 'An error occurred while processing your request. Please try again.'
            return render_template('signup.html', error=error)

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['fullname'] = user.fullname
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid email or password'
    return render_template('login.html', error=error)

@app.route('/welcome')
def welcome():
    # Your existing logic to prepare the game state
    # Reset any session variables if necessary or set defaults
    return render_template('welcome.html', initialSheep=1, initialWolves=1)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
