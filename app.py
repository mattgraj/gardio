from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Home route (index page)
@app.route('/')
def home():
    return render_template('index.html')  # index.html needs to be in the templates folder

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Perform login logic here (e.g., check database)
        if username == "admin" and password == "admin":
            return redirect(url_for('dashboard'))
        else:
            return "Login failed. Try again."
    return render_template('login.html')  # login.html should be in the templates folder

# Dashboard route (after login)
@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == "__main__":
    app.run(debug=True)
