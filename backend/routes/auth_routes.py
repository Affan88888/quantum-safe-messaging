from flask import Blueprint, request, jsonify, session
from models.user_model import create_user, get_user_by_email, get_user_by_email_or_username, check_auth_status, update_user_public_key
from utils.helpers import encrypt_session
from werkzeug.security import check_password_hash
import oqs
import os
from pathlib import Path
from dotenv import set_key  # Use python-dotenv to manage .env files
import base64

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'All fields are required'}), 400

    # Create the user in the database
    if create_user(username, email, password):
        # Generate the client's key pair for session encryption/decryption
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key_client = client.generate_keypair()
            private_key_client = client.export_secret_key()  # Export the private key

        # Fetch the newly created user from the database
        user = get_user_by_email(email)
        if not user:
            return jsonify({'error': 'Failed to retrieve user after registration'}), 500

        # Encrypt session data using the utility function
        encrypted_session = encrypt_session(user['id'], public_key_client)

        # Store session data securely
        session['encrypted_session_data'] = encrypted_session['encrypted_session_data']
        session['encapsulated_key'] = encrypted_session['encapsulated_key']
        session['private_key'] = private_key_client

        # Generate an additional public/private key pair for message encryption/decryption
        with oqs.KeyEncapsulation(kemalg) as message_keygen:
            public_key_message = message_keygen.generate_keypair()
            private_key_message = message_keygen.export_secret_key()

        # Encode keys as Base64
        public_key_message_base64 = base64.b64encode(public_key_message).decode('utf-8')
        private_key_message_base64 = base64.b64encode(private_key_message).decode('utf-8')

        # Store the public key in the database
        update_user_public_key(user['id'], public_key_message_base64)

        # Store the private key in a .env file
        private_keys_dir = Path("private_keys")
        private_keys_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
        env_file_path = private_keys_dir / f"user_{user['id']}.env"

        # Write the private key to the .env file
        set_key(str(env_file_path), f"PRIVATE_KEY_USER_{user['id']}", private_key_message_base64)

        # Return user details along with success message
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'theme': user['theme'],  # Include the theme property
                'public_key_message': public_key_message_base64  # Include the public key for message encryption
            }
        }), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('email')  # from frontend, can be username or email
    password = data.get('password')

    if not all([identifier, password]):
        return jsonify({'error': 'Username/email and password are required'}), 400

    user = get_user_by_email_or_username(identifier)

    if user and check_password_hash(user['password_hash'], password):
        # Generate the client's key pair
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key_client = client.generate_keypair()
            private_key_client = client.export_secret_key()  # Export the private key

        # Encrypt session data using the utility function
        encrypted_session = encrypt_session(user['id'], public_key_client)

        # Store session data securely
        session['encrypted_session_data'] = encrypted_session['encrypted_session_data']
        session['encapsulated_key'] = encrypted_session['encapsulated_key']
        session['private_key'] = private_key_client

        # Return user details along with success message
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'theme': user['theme']  # Include the theme property
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    user_data = check_auth_status(session)
    if user_data:
        return jsonify({
            'authenticated': True,
            'user': user_data
        }), 200
    return jsonify({'authenticated': False}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200