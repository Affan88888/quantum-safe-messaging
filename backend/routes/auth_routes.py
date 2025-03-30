# routes/auth_routes.py

from flask import Blueprint, request, jsonify, session
from models.user_model import create_user, get_user_by_email, check_auth_status
from utils.helpers import encrypt_data, kem
from werkzeug.security import check_password_hash
import oqs
import os
import base64

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if create_user(username, email, password):
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        # Initialize the KEM object for the client
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            # Generate the client's key pair
            public_key_client = client.generate_keypair()
            private_key_client = client.export_secret_key()  # Export the private key

        # Simulate the server encapsulating the shared secret
        with oqs.KeyEncapsulation(kemalg) as server:
            ciphertext, shared_secret_server = server.encap_secret(public_key_client)

        # Use the shared secret as the session key
        session_key = shared_secret_server[:32]
        print("Session key (encryption):", session_key)

        # Encrypt session data
        encrypted_session_data = encrypt_data(session_key, str(user['id']))

        # Store session data
        session['encrypted_session_data'] = base64.b64encode(encrypted_session_data).decode('utf-8')
        session['encapsulated_key'] = base64.b64encode(ciphertext).decode('utf-8')
        session['private_key'] = private_key_client  # Store the private key securely

        # Return the user details along with the success message
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
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