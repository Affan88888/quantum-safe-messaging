from datetime import datetime
from utils.db import get_db_connection
from datetime import datetime
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import dotenv_values
from pathlib import Path
from utils.helpers import decrypt_message
from models.user_model import get_recipient_id_from_chat_for_decryption

def save_message_to_db(chat_id, sender_id, encrypted_message_data):
    """
    Save an encrypted message to the database.
    Returns the ID of the newly inserted message if successful, None otherwise.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()

        # Extract encapsulated_key and encrypted_message from the input
        encapsulated_key = encrypted_message_data['encapsulated_key']
        encrypted_message = encrypted_message_data['encrypted_message']  # Already Base64-encoded

        # Insert the message into the database
        query = """
        INSERT INTO messages (chat_id, sender_id, encrypted_message, encapsulated_key, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                chat_id,
                sender_id,
                encrypted_message,  # Store the entire encrypted message
                encapsulated_key,   # Store the encapsulated key
                datetime.utcnow()   # Use UTC time for consistency
            )
        )
        connection.commit()

        # Retrieve the auto-generated ID of the inserted message
        message_id = cursor.lastrowid
        return message_id
    
    except Exception as e:
        print(f"Error saving message to DB: {e}")
        connection.rollback()
        return None

    finally:
        cursor.close()
        connection.close()

def get_chat_history_from_db(user_id, chat_id):
    """
    Retrieve chat history for a specific chat and decrypt the messages.
    Returns a list of decrypted messages.
    """
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT m.id, m.sender_id, u.username AS sender_username, 
               m.encrypted_message, m.encapsulated_key, m.created_at
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.chat_id = %s
        ORDER BY m.created_at ASC
        """
        cursor.execute(query, (chat_id,))
        raw_messages = cursor.fetchall()

        # Fetch the private key for decryption
        private_keys_dir = Path("private_keys")

        # Helper function to fetch a private key
        def fetch_private_key(user_id_to_fetch):
            env_file_path = private_keys_dir / f"user_{user_id_to_fetch}.env"
            if not env_file_path.exists():
                raise ValueError(f"Private key file not found for user {user_id_to_fetch}")
            env_vars = dotenv_values(env_file_path)
            private_key_base64 = env_vars.get(f"PRIVATE_KEY_USER_{user_id_to_fetch}")
            if not private_key_base64:
                raise ValueError(f"Private key not found in .env file for user {user_id_to_fetch}")
            return base64.b64decode(private_key_base64)

        # Get the current user's private key
        current_user_private_key = fetch_private_key(user_id)

        # Decrypt each message
        decrypted_messages = []
        for msg in raw_messages:
            # Decode the Base64-encoded encrypted_message
            encrypted_message = base64.b64decode(msg['encrypted_message'])

            # Prepare the encrypted message data for decryption
            encrypted_message_data = {
                'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),  # Pass the full encrypted_message
                'encapsulated_key': msg['encapsulated_key']  # Include the encapsulated_key
            }

            try:
                # Ensure consistent data types for comparison
                sender_id = int(msg['sender_id'])
                current_user_id = int(user_id)

                # Determine if the current user is the sender or recipient
                if sender_id == current_user_id:
                    # Current user is the sender; use the recipient's private key
                    recipient_id = get_recipient_id_from_chat_for_decryption(chat_id, user_id)
                    if not recipient_id:
                        raise ValueError("Recipient ID could not be determined.")
                    private_key_to_use = fetch_private_key(recipient_id)
                else:
                    # Current user is the recipient; use their own private key
                    private_key_to_use = current_user_private_key

                # Decrypt the message content using the appropriate private key
                decrypted_content = decrypt_message(encrypted_message_data, private_key_to_use)

            except Exception as e:
                print(f"Failed to decrypt message ID {msg['id']}: {e}")
                decrypted_content = "[Decryption failed]"

            # Append the decrypted message to the result list
            decrypted_messages.append({
                'id': msg['id'],
                'sender_id': msg['sender_id'],
                'sender_username': msg['sender_username'],
                'content': decrypted_content,
                'created_at': msg['created_at']
            })

        return decrypted_messages

    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []
    finally:
        cursor.close()
        connection.close()