from utils.db import get_db_connection

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

        # Query to fetch chats with dynamically generated names
        query = """
        SELECT 
            c.id AS id,
            u.username AS name, -- Get the name of the other participant
            m.content AS last_message,
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
            c.id, u.username, m.content, m.created_at
        ORDER BY 
            MAX(m.created_at) DESC;
        """

        cursor.execute(query, (user_id,))
        chats = cursor.fetchall()  # Fetch all matching chats

        # Post-process the results to ensure only the latest message is included
        chats_with_last_message = []
        seen_chat_ids = set()

        for chat in chats:
            if chat['id'] not in seen_chat_ids:
                chats_with_last_message.append(chat)
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