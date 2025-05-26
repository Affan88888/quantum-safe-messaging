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

def get_recipient_id_from_chat(chat_id, sender_id):
    """
    Retrieve the recipient's user ID from the chat participants.

    Args:
        chat_id (int): The ID of the chat.
        sender_id (int): The ID of the sender (current user).

    Returns:
        int: The recipient's user ID, or None if the recipient cannot be determined.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        # Query to fetch the participants of the chat
        query = """
        SELECT user_id FROM chat_participants WHERE chat_id = %s
        """
        cursor.execute(query, (chat_id,))
        participants = cursor.fetchall()
        print("Participants fetched from DB:", participants)

        # Extract user IDs from the result and ensure they are integers
        participant_ids = [int(participant['user_id']) for participant in participants]
        print("Participant IDs extracted:", participant_ids)

        # Validate the number of participants
        if len(participant_ids) != 2:
            print(f"Unexpected number of participants ({len(participant_ids)}) for chat_id {chat_id}")
            return None

        # Ensure sender_id is an integer
        sender_id = int(sender_id)
        print("Sender ID:", sender_id)

        # Find the recipient ID by excluding the sender's ID
        filtered_ids = [user_id for user_id in participant_ids if user_id != sender_id]
        print("Filtered recipient IDs:", filtered_ids)

        if len(filtered_ids) != 1:
            print("Error: Unable to determine a unique recipient ID.")
            return None

        recipient_id = filtered_ids[0]
        print("Recipient ID determined:", recipient_id)

        return recipient_id

    except Exception as e:
        print(f"Error fetching recipient ID: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def get_user_public_key(user_id):
    """
    Retrieve the public key of a user from the database.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bytes: The user's public key, or None if it cannot be found.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        # Query to fetch the public key of the user
        query = "SELECT public_key_message FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result and result['public_key_message']:
            # Decode the Base64-encoded public key
            return base64.b64decode(result['public_key_message'])

        return None

    except Exception as e:
        print(f"Error fetching user public key: {e}")
        return None

    finally:
        cursor.close()
        connection.close()

def get_recipient_id_from_chat_for_decryption(chat_id, user_id):
    """
    Retrieve the recipient's user ID from the chat participants.
    Assumes a 1-on-1 chat where there are only two participants.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT user_id
        FROM chat_participants
        WHERE chat_id = %s AND user_id != %s
        """
        cursor.execute(query, (chat_id, user_id))
        result = cursor.fetchone()
        return result['user_id'] if result else None
    except Exception as e:
        print(f"Error fetching recipient ID: {e}")
        return None
    finally:
        cursor.close()
        connection.close()