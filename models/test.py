from database import Database

db = Database()

print("Testing database connection...")
db.connect()

# db.get_user('vyomrohila')

print(db.get_hashed_password('vyom'))