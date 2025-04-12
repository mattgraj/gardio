from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import random
import string

app = Flask(__name__)

# Set your secret key for session and CSRF protection
app.config['SECRET_KEY'] = 'gAAAAABn-hC3Wv1ZuylTbtEvVt1myYG4gTuzYldWxcEzpkCJSCeYewnIw9ijBswaG8BwTk5QHivMjcESgfR2hW-Nht92rMDGv77r0nFs_uvuGcDGFz29fT9PohX4gpFFQXKwGme5QGB82mO_YP-_aqj3oifVQASe8hGHUyIazhcqsNStKZBWxM4a9TA-u9_36VhtzJenK017lzKJ3kOa7LxyMxWfDu5_v9ujQ6KupYoyze1vIQWpTyjRy4k64f2BquWyOR5EY4Do_HIQm4HTicGFr2oFK8TJ0PGoTFNEJcTF1uwF8CE2UUb1-6n3uKwJNwr45dwPDp9nth6xOGvfrHnUbRyuqCmwrvG41F5QCgtWdMI9-nf5bxDBWSK3N_6tRE9c2aKtHpnRfvYN8iiNYCYuJB_GyboXHw=='  # Use your secret key here

# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail SMTP server
app.config['MAIL_PORT'] = 465  # Gmail SMTP port
app.config['MAIL_USERNAME'] = 'yinkaj045@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'uxkc ypmp jhoa kqcz'  # Your app password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'yinkaj045@gmail.com'  # Default sender

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
        # Generate token
        token = generate_verification_token()
        # Send email
        send_verification_email(email, token)
        # Store the token in a real app (e.g., database) to verify later
        flash("A verification email has been sent. Please check your inbox.")
        return redirect(url_for('home'))
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Here, you would check the user credentials in a real app
        token = generate_verification_token()
        send_verification_email(email, token)
        flash("A verification email has been sent. Please check your inbox.")
        return redirect(url_for('home'))
    return render_template('login.html')

# Verification route
@app.route('/verify/<token>')
def verify(token):
    # In a real app, you'd compare the token to the stored one in the database
    # For now, we'll assume the token is valid and redirect to a success page.
    return "Your email has been successfully verified!"

if __name__ == "__main__":
    port = os.getenv("PORT", 5000)  # Use the PORT environment variable, default to 5000 if not set
    app.run(debug=True, host='0.0.0.0', port=port)
