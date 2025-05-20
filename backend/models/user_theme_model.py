from utils.db import get_db_connection

def update_user_theme(user_id, theme):
    """
    Update the theme preference for a user in the database.

    Args:
        user_id (int): The ID of the user whose theme is being updated.
        theme (str): The new theme preference ('light' or 'dark').

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        query = "UPDATE users SET theme = %s WHERE id = %s"
        cursor.execute(query, (theme, user_id))
        connection.commit()

        # Check if any rows were affected
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating user theme: {e}")
        return False
    finally:
        cursor.close()
        connection.close()