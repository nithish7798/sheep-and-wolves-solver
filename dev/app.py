from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from collections import deque
from semanticnetsagent import SemanticNetsAgent, State

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
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        if user:
            fullname = user.fullname
            return render_template('welcome.html', fullname=fullname)
        else:
            session.clear()
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    
@app.route('/solution', methods=['POST'])
def solution():
    print("Solution function called")  # Add this line
    try:
        if request.is_json:
            data = request.get_json()
            initialSheep = int(data['initialSheep'])
            initialWolves = int(data['initialWolves'])
        else:
            initialSheep = int(request.form['initialSheep'])
            initialWolves = int(request.form['initialWolves'])
    except KeyError:
        return jsonify({'error': 'Missing input data'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid input data. Please provide integers for initialSheep and initialWolves'}), 400

    agent = SemanticNetsAgent()
    solution = agent.solve(initialSheep, initialWolves)
    print("Solution:", solution)  # Add this line to print the solution
    return jsonify(solution)




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)
