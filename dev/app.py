# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import check_password_hash
# from flask_bcrypt import Bcrypt,check_password_hash
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Initialize Flask-Migrate
# migrate = Migrate(app, db)

# from models import User

# @app.route('/')
# def home():
#     return render_template('signup.html')

# bcrypt = Bcrypt(app)

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         fullname= request.form['fullname']
#         email = request.form['email']
#         password = request.form['password']
#         print("||||email|||||",email)
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(fullname=fullname,email=email, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('signup.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None  # Initialize error variable
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         user = User.query.filter_by(email=email).first()
#         if user and bcrypt.check_password_hash(user.password, password):
#             session['user_id'] = user.id
#             session['fullname'] = user.fullname  # Pass the full name to the session
#             return redirect(url_for('welcome'))
#         else:
#             error = 'Invalid email or password'  # Set the error message
#     return render_template('login.html', error=error)

# @app.route('/welcome')
# def welcome():
#     if 'user_id' in session:
#         fullname = session['fullname']  # Retrieve full name from session
#         return render_template('welcome.html', fullname=fullname)
#     else:
#         return redirect(url_for('login'))


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import User model after db creation
from models import User

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname= request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(fullname=fullname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error variable
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['fullname'] = user.fullname  # Pass the full name to the session
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid email or password'  # Set the error message
    return render_template('login.html', error=error)  # Pass error message to template


@app.route('/welcome')
def welcome():
    if 'user_id' in session:
        fullname = session['fullname']  # Retrieve full name from session
        return render_template('welcome.html', fullname=fullname)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove 'user_id' from session
    session.pop('fullname', None)  # Remove 'fullname' from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
