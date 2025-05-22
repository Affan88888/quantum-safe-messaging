# routes/auth_routes.py

from flask import Blueprint, request, jsonify, session
from models.user_model import create_user, get_user_by_email, check_auth_status  # ✅ Added check_auth_status
from utils.helpers import encrypt_session
from passlib.hash import argon2
import oqs
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

    if create_user(username, email, password):
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key_client = client.generate_keypair()
            private_key_client = client.export_secret_key()

        user = get_user_by_email(email)
        encrypted_session = encrypt_session(user['id'], public_key_client)

        # 🔐 Store private key as base64-encoded string
        session['private_key'] = base64.b64encode(private_key_client).decode()
        session['encrypted_session_data'] = encrypted_session['encrypted_session_data']
        session['encapsulated_key'] = encrypted_session['encapsulated_key']

        session.modified = True
        session.permanent = True  # Keeps session alive across refreshes

        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }), 201
    else:
        return jsonify({'error': 'Username or email already exists'}), 409

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Email and password are required'}), 400

    user = get_user_by_email(email)
    if user and argon2.verify(password, user['password_hash']):
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key_client = client.generate_keypair()
            private_key_client = client.export_secret_key()

        encrypted_session = encrypt_session(user['id'], public_key_client)

        # 🔐 Store private key as base64-encoded string
        session['private_key'] = base64.b64encode(private_key_client).decode()
        session['encrypted_session_data'] = encrypted_session['encrypted_session_data']
        session['encapsulated_key'] = encrypted_session['encapsulated_key']

        session.modified = True
        session.permanent = True  # Keeps session alive across refreshes

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