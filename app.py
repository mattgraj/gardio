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

# Secret key for sessions and security
app.config['SECRET_KEY'] = 'gAAAAABn-hI7Mt04QoUIz0k0mu5lzEJcuWUTYDcU5DbFkxXJotcl5AlGljQ7pIhHY0J8YupUa6vXnlY4GEeOYRXNH2EnTo8S-CkVg9DIBvyPhxAQ_dqwp0Dcuwd9P2dumzafy5zL-oW-wYgsUv0icUHMuwhcwTCuqIv04zkZA2KASzlCxTrz4ILNU0pCf-gkabC_NU1gQpM10hnaSxKVD4c5WFkQSIdeER-d2MtCWzuAzElujn7kjc0P43tFGaF9aLzAore1iov-M8Pi1IIujtwFpFGs8eL59yqZKgHiNQ6hQxhsEZ79WNlory9PX7mgW_RgVbZp9q2e2ZOmyJTWo-AF59o76Ww3VzEWNTwH4Gglanad_mEi159VlSbzaSzjH5u84EBa9cuJR_xh78Q-2odWuQDqubX2lQ=='

mail = Mail(app)

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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if not username or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('signup'))
        
        # Generate token
        token = generate_verification_token()
        # Send email
        send_verification_email(email, token)
        
        flash("A verification email has been sent. Please check your inbox.", "success")
        return redirect(url_for('login'))  # Redirect to the login page after sign up
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash("Please enter both email and password!", "danger")
            return redirect(url_for('login'))
        
        # Here, you would check the user credentials in a real app
        # For now, we assume the login attempt is valid
        token = generate_verification_token()
        send_verification_email(email, token)
        
        flash("A verification email has been sent. Please check your inbox.", "success")
        return redirect(url_for('home'))  # Redirect to home page after login
    return render_template('login.html')

# Verification route
@app.route('/verify/<token>')
def verify(token):
    # In a real app, you'd compare the token to the stored one in the database
    # For now, we'll assume the token is valid and redirect to a success page.
    return "Your email has been successfully verified!"

if __name__ == "__main__":
    app.run(debug=True)
