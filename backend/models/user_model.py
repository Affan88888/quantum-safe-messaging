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
        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
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
        query = "SELECT id, username, email, password_hash, theme FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_user_by_email_or_username(identifier):
    """Retrieve a user by either email or username."""
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE email = %s OR username = %s"
        cursor.execute(query, (identifier, identifier))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user by email or username: {e}")
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
        query = "SELECT id, username, email, theme FROM users WHERE id = %s"
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
                'email': user['email'],
                'theme': user['theme']  # Include the theme property
            }
    except ValueError as e:
        print(f"Error validating session: {e}")
        return None  # Invalid session data or decryption failure

    return None

def update_user_public_key(user_id, public_key_message_base64):
    """
    Updates the user's public key in the database.

    Args:
        user_id (int): The ID of the user.
        public_key_message_base64 (str): The Base64-encoded public key for message encryption.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    connection = get_db_connection()  # Establish the database connection
    if not connection:
        print("Failed to connect to the database.")
        return False

    try:
        cursor = connection.cursor(dictionary=True)
        query = "UPDATE users SET public_key_message = %s WHERE id = %s"
        cursor.execute(query, (public_key_message_base64, user_id))
        
        # Commit the transaction
        connection.commit()
        
        # Check if any rows were affected by the update
        if cursor.rowcount > 0:
            return True
        else:
            print(f"No rows updated for user_id: {user_id}")
            return False

    except Exception as e:
        print(f"Error updating public key: {e}")
        connection.rollback()  # Rollback in case of error
        return False

    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection