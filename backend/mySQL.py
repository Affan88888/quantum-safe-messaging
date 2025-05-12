import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    try:
        # Step 1: Connect to the MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host='localhost',       # Replace with your MySQL host
            user='root',            # Replace with your MySQL username
            password='password'     # Replace with your MySQL password
        )

        if connection.is_connected():
            print("Connected to MySQL server")

            # Step 2: Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Step 3: Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS quantum_safe_messaging;")
            print("Database 'quantum_safe_messaging' created or already exists.")

            # Step 4: Use the newly created database
            cursor.execute("USE quantum_safe_messaging;")
            print("Using database 'quantum_safe_messaging'.")

            # Step 5: Create the 'users' table with the new 'theme' column
            create_users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                theme ENUM('light', 'dark') DEFAULT 'light',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_users_table_query)
            print("Table 'users' created or already exists.")

            # Step 6: Check if the 'theme' column exists and add it if it doesn't
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'theme';
            """)
            column_exists = cursor.fetchone()[0]

            if not column_exists:
                alter_users_table_query = """
                ALTER TABLE users ADD COLUMN theme ENUM('light', 'dark') DEFAULT 'light';
                """
                cursor.execute(alter_users_table_query)
                print("Column 'theme' added to table 'users'.")
            else:
                print("Column 'theme' already exists in table 'users'.")

            # Step 7: Create the 'chats' table
            create_chats_table_query = """
            CREATE TABLE IF NOT EXISTS chats (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255), -- Optional: For naming group chats
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_chats_table_query)
            print("Table 'chats' created or already exists.")

            # Step 8: Create the 'chat_participants' table
            create_chat_participants_table_query = """
            CREATE TABLE IF NOT EXISTS chat_participants (
                chat_id INT NOT NULL,
                user_id INT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (chat_id, user_id),
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_chat_participants_table_query)
            print("Table 'chat_participants' created or already exists.")

            # Step 9: Create the 'messages' table
            create_messages_table_query = """
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id INT NOT NULL,
                sender_id INT NOT NULL,
                content TEXT NOT NULL, -- The text content of the message
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
                FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_messages_table_query)
            print("Table 'messages' created or already exists.")

            # Step 10: Create the 'user_contacts' table
            create_user_contacts_table_query = """
            CREATE TABLE IF NOT EXISTS user_contacts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                contact_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (contact_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE (user_id, contact_id) -- Ensures no duplicate contacts for the same user
            );
            """
            cursor.execute(create_user_contacts_table_query)
            print("Table 'user_contacts' created or already exists.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Step 11: Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# Call the function to execute the script
create_database_and_table()