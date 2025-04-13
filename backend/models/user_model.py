from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
from utils.helpers import decrypt_session
import base64
import oqs

def create_user(username, email, password):
    """Create a new user in the database."""
    password_hash = generate_password_hash(password)
    connection = get_db_connection()
    if not connection:
        return False

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


def get_user_by_email(email):
    """Retrieve a user from the database by email."""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def get_user_by_id(user_id):
    """Retrieve a user from the database by ID."""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()


def check_auth_status(session):
    """
    Validate the session and retrieve the authenticated user's details.

    Args:
        session (dict): The session object containing encrypted session data,
                        encapsulated key, and private key.

    Returns:
        dict or None: User details if the session is valid, otherwise None.
    """
    try:
        # Decrypt the session to retrieve the user_id using the decrypt_session function
        user_id = decrypt_session(session)

        # Fetch user details from the database using the decrypted user_id
        user = get_user_by_id(user_id)

        if user:
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
    except ValueError as e:
        print(f"Error validating session: {e}")
        return None  # Invalid session data or decryption failure

    return None