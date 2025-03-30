# routes/auth_routes.py

from flask import Blueprint, request, jsonify, session
from models.user_model import create_user, get_user_by_email, check_auth_status
from utils.helpers import encrypt_data, kem
from werkzeug.security import check_password_hash
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
        # Generate a key pair for KEM
        public_key = kem.generate_keypair()

        # Encapsulate the shared secret
        shared_secret, encapsulated_key = kem.encap_secret(public_key)

        # Use the shared secret as the session key
        session_key = shared_secret[:32]
        print("Session key:", session_key)
        x = b'n\xe8h2.&\xd1,Y\xa3\xd8\x8fj\x0b\xb0~\xa77\x84\xdf\xffH\xdf)\xc7\xf5\xedX\x91\x1ch\x86'

        # Encrypt session data
        encrypted_session_data = encrypt_data(x, str(user['id']))

        # Encode binary data as Base64 before storing in the session
        session['encrypted_session_data'] = base64.b64encode(encrypted_session_data).decode('utf-8')
        session['encapsulated_key'] = base64.b64encode(encapsulated_key).decode('utf-8')

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