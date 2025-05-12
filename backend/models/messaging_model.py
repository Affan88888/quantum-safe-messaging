from datetime import datetime
from utils.db import get_db_connection
from datetime import datetime

def save_message_to_db(chat_id, sender_id, content):
    """
    Save a message to the database.
    Returns the ID of the newly inserted message if successful, None otherwise.
    """
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO messages (chat_id, sender_id, content, created_at)
        VALUES (%s, %s, %s, %s)
        """
        # Use datetime.utcnow() to save the current GMT/UTC time
        cursor.execute(query, (chat_id, sender_id, content, datetime.utcnow()))
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
    Retrieve chat history for a specific chat.
    Returns a list of messages.
    """
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT m.id, m.sender_id, u.username AS sender_username, m.content, m.created_at
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.chat_id = %s
        ORDER BY m.created_at ASC
        """
        cursor.execute(query, (chat_id,))
        messages = cursor.fetchall()
        return messages
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
