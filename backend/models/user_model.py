# models/user_model.py

from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
from utils.helpers import kem, decrypt_data
import base64

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

def get_user_by_id(user_id):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    return None

def check_auth_status(session):
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')

    if not encrypted_session_data or not encapsulated_key:
        return None  # Session data is missing or invalid

    try:
        # Decode Base64-encoded session data back to binary
        encrypted_session_data = base64.b64decode(encrypted_session_data)
        encapsulated_key = base64.b64decode(encapsulated_key)

        # Decapsulate the shared secret
        shared_secret = kem.decap_secret(encapsulated_key)

        # Use the shared secret as the session key
        session_key = shared_secret[:32]
        print("Shared secret (decryption):", session_key)
        x = b'n\xe8h2.&\xd1,Y\xa3\xd8\x8fj\x0b\xb0~\xa77\x84\xdf\xffH\xdf)\xc7\xf5\xedX\x91\x1ch\x86'

        # Decrypt the session data
        user_id = decrypt_data(x, encrypted_session_data)
        print("user_id:", user_id)

        # Fetch user details from the database using the decrypted user_id
        user = get_user_by_id(user_id)
        print("user: ", user)
        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
    except Exception as e:
        print(f"Error validating session: {e}")
        return None  # Invalid session data or decryption failure

    return None