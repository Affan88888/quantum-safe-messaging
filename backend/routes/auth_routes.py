# routes/auth_routes.py

from flask import Blueprint, request, jsonify, session
from models.user_model import create_user, get_user_by_email
from utils.helpers import encrypt_data, kem
from werkzeug.security import check_password_hash
import os

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
        # Generate a session key
        session_key = os.urandom(32)  # 256-bit key for AES

        # Use the pre-initialized `kem` object from utils.helpers
        public_key = kem.generate_keypair()
        ciphertext, encapsulated_key = kem.encap_secret(public_key)

        # Encrypt session data
        encrypted_session_data = encrypt_data(session_key, str(user['id']))

        # Store session data
        session['encrypted_session_data'] = encrypted_session_data
        session['encapsulated_key'] = encapsulated_key

        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200