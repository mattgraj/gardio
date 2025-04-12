from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import string
import sqlite3

app = Flask(__name__)

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yinkaj045@gmail.com'
app.config['MAIL_PASSWORD'] = 'uxkc ypmp jhoa kqcz'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'yinkaj045@gmail.com'
app.secret_key = 'your_secret_key'  # Secret key for flashing messages

mail = Mail(app)

# Database setup
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create user table if it doesn't exist
def create_table():
    with get_db() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            verified BOOLEAN NOT NULL DEFAULT 0,
            token TEXT
        )
        """)

create_table()

# Generate a random verification token
def generate_verification_token(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

# Send verification email
def send_verification_email(user_email, token):
    verification_url = f"http://127.0.0.1:5000/verify/{token}"
    msg = Message("Email Verification", recipients=[user_email])
    msg.body = f"Please click the link to verify your email: {verification_url}"
    try:
        mail.send(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the user already exists
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if user:
                message = "This email is already registered."
                return render_template('signup.html', message=message)

        # Hash the password
        hashed_password = generate_password_hash(password)
        
        # Store user data (email and hashed password) in the database
        with get_db() as db:
            db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        
        # Generate token
        token = generate_verification_token()
        
        # Store token in the database
        with get_db() as db:
            db.execute("UPDATE users SET token = ? WHERE email = ?", (token, email))
        
        # Send verification email
        send_verification_email(email, token)
        
        message = "A verification email has been sent. Please check your inbox."
        flash(message)
        return redirect(url_for('home'))
    
    return render_template('signup.html', message=message)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if the email exists in users
        with get_db() as db:
            user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            if not user:
                message = "Email not registered."
                return render_template('login.html', message=message)

            # Check if the password is correct
            if not check_password_hash(user['password'], password):
                message = "Invalid password."
                return render_template('login.html', message=message)
        
        # Generate and send verification code
        token = generate_verification_token()
        with get_db() as db:
            db.execute("UPDATE users SET token = ? WHERE email = ?", (token, email))
        
        send_verification_email(email, token)

        # Ask the user to enter the verification token
        message = "A verification code has been sent to your email. Please check your inbox."
        return render_template('verify_token.html', message=message, email=email)

    return render_template('login.html', message=message)

# Verify token route
@app.route('/verify/<token>', methods=['GET'])
def verify(token):
    email = request.args.get('email')
    
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and user['token'] == token:
            db.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
            return f"Your email ({email}) has been successfully verified!"
    
    return "Invalid verification token."

# Verify token form route (for the user to enter the code)
@app.route('/verify_token', methods=['POST'])
def verify_token():
    email = request.form['email']
    token = request.form['token']
    
    with get_db() as db:
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and user['token'] == token:
            db.execute("UPDATE users SET verified = 1 WHERE email = ?", (email,))
            return f"Your email ({email}) has been successfully verified!"
    
    return "Invalid verification token."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
