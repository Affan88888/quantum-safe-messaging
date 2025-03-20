import mysql.connector
from mysql.connector import Error

def create_database_and_table():
    try:
        # Step 1: Connect to the MySQL server (without specifying a database)
        connection = mysql.connector.connect(
            host='localhost',       # Replace with your MySQL host
            user='affan',            # Replace with your MySQL username
            password='Venvscripts333_'  # Replace with your MySQL password
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

            # Step 5: Create the 'users' table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            print("Table 'users' created or already exists.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Step 6: Close the cursor and connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# Call the function to execute the script
create_database_and_table()