from utils.db import get_db_connection

def add_contact_to_user(user_id, contact_id):
    """
    Add a contact to the user's list of contacts.
    Returns True if successful, False otherwise.
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO user_contacts (user_id, contact_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE user_id = user_id
        """
        cursor.execute(query, (user_id, contact_id))
        connection.commit()
        return True
    except Exception as e:
        print(f"Error adding contact: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
        connection.close()


def get_contacts_for_user(user_id):
    """
    Retrieve the list of contacts for the given user_id.
    Returns a list of contact details (id, username, email).
    """
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)  # Use dictionary=True for easier JSON serialization
        query = """
        SELECT c.id, c.username, c.email
        FROM user_contacts uc
        JOIN users c ON uc.contact_id = c.id
        WHERE uc.user_id = %s
        """
        cursor.execute(query, (user_id,))
        contacts = cursor.fetchall()  # Fetch all matching contacts
        return contacts

    except Exception as e:
        print(f"Error fetching contact list: {e}")
        return []

    finally:
        cursor.close()
        connection.close()