from flask import Flask, request, redirect, url_for, session, flash, render_template, make_response, g
from flask_login import current_user
from dotenv import load_dotenv
from functools import wraps
from models.database import Database
from models.jwt import JWT
import os
import bcrypt

load_dotenv()
app = Flask(__name__, template_folder="../templates")
app.secret_key = os.getenv('flask_secret_key')
db = Database()
jwt = JWT()

@app.route('/')
@jwt.check_token
def dashboard():
    return render_template('dashboard.html', current_user=g.current_user)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('login'))
        
        user = db.get_user(username)
        if user:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            db_password = db.get_hashed_password(username)
            if db_password:
                db_password = db_password[0]
                if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                    flash('Login successful!', 'success')
                    role = db.get_role(username)
                    token = jwt.generate_token(username, role)
                    response = make_response(redirect(url_for('dashboard')))
                    response.set_cookie('access_token', token, httponly=True)
                    return response
                else:
                    flash(db_password, 'error')
                    return redirect(url_for('login'))
            else:
                flash('Failed to retrieve user password.', 'error')
                return redirect(url_for('login'))
        else:
            flash(user)
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('register'))
        
        existing_user = db.get_user(username)
        if existing_user:
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        result = db.add_user(username, hashed_password.decode('utf-8'))
        
        if result == "User added successfully.":
            flash(result, 'success')
            return redirect(url_for('login'))
        else:
            flash(result, 'error')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')
    
@app.route('/logout')
@jwt.check_token
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('access_token', '', expires=0)
    flash('You have been logged out.', 'success')
    return response