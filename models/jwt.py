import jwt
from dotenv import load_dotenv
from functools import wraps
from flask import request, flash, redirect, url_for, g
import os
from datetime import datetime, timedelta, timezone

load_dotenv()
class JWT:
    def __init__(self):
        self.jwt_secret_key = os.getenv('jwt_secret_key')
        
    def generate_token(self, username, role):
        payload = {
            'username' : username,
            'role' : role,
            'exp' : datetime.now().astimezone() + timedelta(hours=1)
        }
        token = jwt.encode(payload, self.jwt_secret_key, algorithm='HS256')
        return token
    
    # def check_token(self, token):
    #     try:
    #         payload = jwt.decode(token, self.jwt_secret_key, algorithms='HS256')
    #         return payload
    #     except jwt.ExpiredSignatureError:
    #         return "Token has expired."
    #     except jwt.InvalidTokenError:
    #         return "Invalid token."
    
    def check_token(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.cookies.get('access_token')
            if not token:
                flash("Access token is missing.", 'error')
                return redirect(url_for('login'))
            
            try:
                payload = jwt.decode(token, os.getenv('jwt_secret_key'), algorithms=['HS256'])
                g.current_user = payload
                return f(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return "Token has expired.", 401
            except jwt.InvalidTokenError:
                return "Invalid token.", 401
            
        return decorated_function   