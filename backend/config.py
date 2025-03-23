# config.py

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Default to 'localhost' if not set
    'user': os.getenv('DB_USER', 'root'),       # Default to 'root' if not set
    'password': os.getenv('DB_PASSWORD', ''),   # No default password
    'database': os.getenv('DB_NAME', 'quantum_safe_messaging')  # Default database name
}

# Secret key for session management
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')