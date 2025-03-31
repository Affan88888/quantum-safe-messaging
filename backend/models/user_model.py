from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
from utils.helpers import decrypt_data
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
    # Retrieve session data
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')
    private_key = session.get('private_key')

    # Ensure all required session data is present
    if not all([encrypted_session_data, encapsulated_key, private_key]):
        return None  # Session data is missing or invalid

    try:
        # Decode Base64-encoded session data back to binary
        encrypted_session_data = base64.b64decode(encrypted_session_data)
        encapsulated_key = base64.b64decode(encapsulated_key)

        # Initialize the KEM object with the private key
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg, private_key) as client:
            # Decapsulate the shared secret using the private key
            shared_secret = client.decap_secret(encapsulated_key)

        # Use the first 32 bytes of the shared secret as the session key
        session_key = shared_secret[:32]

        # Decrypt the session data using the session key
        user_id = decrypt_data(session_key, encrypted_session_data)

        # Fetch user details from the database using the decrypted user_id
        user = get_user_by_id(user_id)

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