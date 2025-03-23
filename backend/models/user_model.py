# models/user_model.py

from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection

def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, password_hash))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    return False

def get_user_by_email(email):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None