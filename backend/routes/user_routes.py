# routes/user_routes.py

from flask import Blueprint, jsonify, session
from utils.helpers import decrypt_data, kem

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')

    if not encrypted_session_data or not encapsulated_key:
        return jsonify({'error': 'Unauthorized'}), 401

    session_key = kem.decapsulate(encapsulated_key)
    user_id = decrypt_data(session_key, encrypted_session_data)

    return jsonify({'message': f'Welcome, user {user_id}!'})