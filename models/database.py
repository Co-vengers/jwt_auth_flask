import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
class Database:
    def __init__(self):  
        self.connection = None
        self.connect()
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = os.getenv('db_host'),
                user = os.getenv('db_user'),
                password = os.getenv('db_password'),
                database = os.getenv('db_name')  
            )
            if self.connection.is_connected():
                print("Successfully connected to the database.")
                return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection = None
            
    def add_user(self, username, password):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO auth (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))  # Fixed query tuple usage
            self.connection.commit()
            self.close()
            return "User added successfully."
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
            self.close()
            return "Failed to add user."
    
    def get_user(self, username):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "SELECT username FROM auth WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            self.close()
            print(f"Retrieved user: {user}")
            return user
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.close()
            return "Failed to retrieve user."
        
    def get_hashed_password(self, username):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "SELECT password FROM auth WHERE username = %s"
            cursor.execute(query, (username,))  # Fixed query tuple usage
            hashed_password = cursor.fetchone()
            self.close()
            return hashed_password
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.close()
            return "Failed to retrieve hashed password."
        
    def get_role(self, username):
        if not self.connection or not self.connection.is_connected():
            self.connect()
        try:
            cursor = self.connection.cursor()
            query = "SELECT* FROM auth WHERE username = %s"
            cursor.execute(query, (username,))
            role = cursor.fetchone()
            self.close()
            return role
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.close()
            return "Failed to retrieve role."
    
    def close(self):
        if self.connection and self.connection.is_connected():
            print("Closing the database connection.")
            self.connection.close()