from flask import Blueprint, request, jsonify, session
from flask_socketio import SocketIO, emit
from models.messaging_model import save_message_to_db, get_chat_history_from_db
from utils.helpers import decrypt_session
from datetime import datetime

# Create a Blueprint for messaging-related routes
messaging_bp = Blueprint('messaging', __name__)

# Initialize SocketIO
socketio = SocketIO()

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection."""
    try:
        user_id = decrypt_session(session)
        print(f"User {user_id} connected via WebSocket.")
    except ValueError as e:
        print(f"WebSocket connection failed: {e}")
        return False  # Reject connection if session decryption fails

@socketio.on('send_message')
def handle_send_message(data):
    """
    Handle sending a message via WebSocket.
    Save the message to the database and broadcast it to the chat participants.
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

        # Save the message to the database and retrieve the auto-generated ID
        message_id = save_message_to_db(chat_id, sender_id, content)
        if not message_id:
            emit('error', {'message': 'Failed to save message to the database.'})
            return

        # Broadcast the message to all participants in the chat
        emit('receive_message', {
            'id': message_id,  # Include the database-generated ID
            'chat_id': chat_id,
            'sender_id': sender_id,
            'content': content,
            'timestamp': datetime.now().strftime('%I:%M %p')
        }, room=chat_id)  # Use chat_id as the room for broadcasting

        # Emit the message back to the sender for UI updates
        emit('receive_message', {
            'id': message_id,  # Include the database-generated ID
            'chat_id': chat_id,
            'sender_id': sender_id,
            'content': content,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })

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
