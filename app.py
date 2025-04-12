from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import random
import string

app = Flask(__name__)

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 465  # Gmail SMTP port
app.config['MAIL_USERNAME'] = 'yinkaj045@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'uxkc ypmp jhoa kqcz'  # Your app password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'yinkaj045@gmail.com'  # Default sender

mail = Mail(app)

# Store tokens in-memory (you can use a database in production)
tokens = {}

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
        # Generate token
        token = generate_verification_token()
        # Send email
        send_verification_email(email, token)
        # Store the token in memory
        tokens[email] = token
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
        token = request.form['token']
        # Check if the email and token match
        if tokens.get(email) == token:
            message = "Login successful!"
        else:
            message = "Invalid token or email."
    return render_template('login.html', message=message)

# Verification route
@app.route('/verify/<token>')
def verify(token):
    # In a real app, you'd compare the token to the stored one in the database
    # For now, we'll assume the token is valid and redirect to a success page.
    return "Your email has been successfully verified!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=True)
