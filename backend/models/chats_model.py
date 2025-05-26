from utils.db import get_db_connection
import base64
from dotenv import dotenv_values
from pathlib import Path
from utils.helpers import decrypt_message

def get_chats_for_user(user_id):
    """
    Retrieve the list of chats for the given user_id.
    Returns a list of chat details (id, name, last_message, timestamp).
    The chat name is dynamically generated based on the other participant's name.
    """
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for easier JSON serialization

        # Query to fetch chats with dynamically generated names and encrypted messages
        query = """
        SELECT 
            c.id AS id,
            u.username AS name, -- Get the name of the other participant
            m.encrypted_message AS encrypted_message, -- Combined ciphertext and IV
            m.encapsulated_key AS encapsulated_key,
            m.created_at AS timestamp
        FROM 
            chat_participants cp1
        JOIN 
            chat_participants cp2 ON cp1.chat_id = cp2.chat_id AND cp1.user_id != cp2.user_id
        JOIN 
            chats c ON cp1.chat_id = c.id
        JOIN 
            users u ON cp2.user_id = u.id
        LEFT JOIN 
            messages m ON c.id = m.chat_id
        WHERE 
            cp1.user_id = %s
        GROUP BY 
            c.id, u.username, m.encrypted_message, m.encapsulated_key, m.created_at
        ORDER BY 
            MAX(m.created_at) DESC;
        """

        cursor.execute(query, (user_id,))
        raw_chats = cursor.fetchall()  # Fetch all matching chats
        #print("raw_chats: ", raw_chats)

        # Fetch the private key for decryption
        private_keys_dir = Path("private_keys")
        env_file_path = private_keys_dir / f"user_{user_id}.env"
        if not env_file_path.exists():
            raise ValueError(f"Private key file not found for user {user_id}")

        env_vars = dotenv_values(env_file_path)
        private_key_base64 = env_vars.get(f"PRIVATE_KEY_USER_{user_id}")
        if not private_key_base64:
            raise ValueError(f"Private key not found in .env file for user {user_id}")

        private_key_message = base64.b64decode(private_key_base64)

        # Post-process the results to decrypt the latest message for each chat
        chats_with_last_message = []
        seen_chat_ids = set()

        for chat in raw_chats:
            if chat['id'] not in seen_chat_ids:
                # Check if encrypted_message and encapsulated_key are None
                if chat['encrypted_message'] is None or chat['encapsulated_key'] is None:
                    decrypted_content = "[No messages yet]"
                else:
                    # Decode the Base64-encoded encrypted_message
                    try:
                        encrypted_message = base64.b64decode(chat['encrypted_message'])
                    except Exception as e:
                        print(f"Failed to decode encrypted message for chat ID {chat['id']}: {e}")
                        decrypted_content = "[Decryption failed]"
                        continue

                    # Prepare encrypted message data for decryption
                    encrypted_message_data = {
                        'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),  # Pass the full encrypted_message
                        'encapsulated_key': chat['encapsulated_key']
                    }

                    # Decrypt the message
                    try:
                        decrypted_content = decrypt_message(encrypted_message_data, private_key_message)
                    except Exception as e:
                        print(f"Failed to decrypt message for chat ID {chat['id']}: {e}")
                        decrypted_content = "[Decryption failed]"

                # Append the chat with the decrypted message
                chats_with_last_message.append({
                    'id': chat['id'],
                    'name': chat['name'],  # Name of the other participant
                    'last_message': decrypted_content,
                    'timestamp': chat['timestamp'] or "No timestamp available"
                })

                seen_chat_ids.add(chat['id'])

        return chats_with_last_message

    except Exception as e:
        print(f"Error fetching chat list: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

def create_chat(user_id, contact_id):
    """
    Create a new chat between the given user_id and contact_id.
    Returns True if the chat was created successfully, False otherwise.
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Start a transaction
        connection.start_transaction()

        # Check if a chat already exists between the user and the contact
        cursor.execute(
            """
            SELECT c.id AS chat_id
            FROM chat_participants cp1
            JOIN chat_participants cp2 ON cp1.chat_id = cp2.chat_id
            JOIN chats c ON cp1.chat_id = c.id
            WHERE cp1.user_id = %s AND cp2.user_id = %s
            """,
            (user_id, contact_id)
        )
        existing_chat = cursor.fetchone()

        if existing_chat:
            # If a chat already exists, return True (no need to create a new one)
            connection.commit()
            return True

        # Fetch the usernames of both participants
        cursor.execute(
            """
            SELECT username
            FROM users
            WHERE id = %s OR id = %s
            ORDER BY username ASC
            """,
            (user_id, contact_id)
        )
        usernames = cursor.fetchall()

        if len(usernames) != 2:
            # If we don't have exactly two usernames, rollback and exit
            connection.rollback()
            print(f"Error: Unable to fetch usernames for user IDs {user_id} and {contact_id}.")
            return False

        # Extract the usernames and create the chat name
        username1, username2 = usernames[0][0], usernames[1][0]
        chat_name = f"{username1}_{username2}"

        # Create a new chat with the custom name
        cursor.execute(
            "INSERT INTO chats (name) VALUES (%s)",
            [chat_name]
        )
        chat_id = cursor.lastrowid

        # Add the user and contact as participants of the chat
        cursor.execute(
            "INSERT INTO chat_participants (chat_id, user_id) VALUES (%s, %s), (%s, %s)",
            (chat_id, user_id, chat_id, contact_id)
        )

        # Commit the transaction
        connection.commit()
        return True

    except Exception as e:
        # Rollback the transaction in case of an error
        connection.rollback()
        print(f"Error creating chat: {e}")
        return False

    finally:
        cursor.close()
        connection.close()