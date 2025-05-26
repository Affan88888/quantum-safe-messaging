from flask import Blueprint, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room
from models.messaging_model import save_message_to_db, get_chat_history_from_db
from models.chats_model import get_chats_for_user
from models.user_model import get_recipient_id_from_chat, get_user_public_key
from utils.helpers import decrypt_session, encrypt_message
from datetime import datetime

# Create a Blueprint for messaging-related routes
messaging_bp = Blueprint('messaging', __name__)

# Initialize SocketIO
socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    try:
        # Decrypt the session to get the user ID
        user_id = decrypt_session(session)
        print(f"User {user_id} connected via WebSocket.")
        
        # Fetch the list of chats for the user
        user_chats = get_chats_for_user(user_id)  # Fetch chats from the database
        
        # Join the user to each chat room
        for chat in user_chats:
            chat_id = str(chat['id'])  # Convert chat_id to string to ensure consistency
            join_room(chat_id)
            print(f"User {user_id} joined room: {chat_id}")

    except ValueError as e:
        print(f"WebSocket connection failed: {e}")
        return False  # Reject connection if session decryption fails

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handle sending a message via WebSocket.
    Encrypt the message, save it to the database, and broadcast it to the chat participants.
    """
    try:
        # Retrieve sender's user ID from the session
        sender_id = decrypt_session(session)
        
        # Extract chat_id and content from the WebSocket payload
        chat_id = data.get('chat_id')
        content = data.get('content')

        if not chat_id or not content:
            emit('error', {'message': 'Chat ID and content are required.'})
            return

        # Fetch the recipient's public key from the database
        recipient_id = get_recipient_id_from_chat(chat_id, sender_id)
        if not recipient_id:
            emit('error', {'message': 'Failed to determine the recipient.'})
            return

        recipient_public_key = get_user_public_key(recipient_id)
        if not recipient_public_key:
            emit('error', {'message': 'Recipient public key not found.'})
            return

        # Encrypt the message
        encrypted_message_data = encrypt_message(content, recipient_public_key)

        # Save the encrypted message to the database
        message_id = save_message_to_db(
            chat_id,
            sender_id,
            encrypted_message_data
        )
        if not message_id:
            emit('error', {'message': 'Failed to save message to the database.'})
            return

        # Broadcast the encrypted message to all participants in the chat
        emit('receive_message', {
            'id': message_id,
            'chat_id': chat_id,
            'sender_id': sender_id,
            'encrypted_message': encrypted_message_data,
            'timestamp': datetime.now().strftime('%I:%M %p')
        }, room=str(chat_id))  # Use chat_id as the room for broadcasting

    except Exception as e:
        print(f"Error handling send_message event: {e}")
        emit('error', {'message': 'An error occurred while processing the message.'})

@messaging_bp.route('/get-chat-history', methods=['POST'])
def get_chat_history():
    """
    Fetch chat history between the logged-in user and a specific contact.
    """
    try:
        user_id = decrypt_session(session)  # Get user ID from session
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    data = request.json
    chat_id = data.get('chat_id')

    if not chat_id:
        return jsonify({'error': 'Recipient ID is required.'}), 400

    # Fetch chat history from the database
    chat_history = get_chat_history_from_db(user_id, chat_id)
    return jsonify({'chat_history': chat_history}), 200