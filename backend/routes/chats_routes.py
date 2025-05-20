from flask import Blueprint, jsonify, session, request
from models.chats_model import get_chats_for_user, create_chat
from utils.helpers import decrypt_session

# Create a Blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/get-chat-list', methods=['GET'])
def get_chat_list():
    """
    Retrieve the list of chats for the logged-in user.
    """
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Fetch the chat list for the user
    try:
        chats = get_chats_for_user(user_id)
        if not chats:
            return jsonify({'message': 'No chats found.', 'chats': []}), 200

        return jsonify({
            'message': 'Chats retrieved successfully.',
            'chats': chats
        }), 200

    except Exception as e:
        print(f"Error fetching chat list: {e}")
        return jsonify({'error': 'An error occurred while fetching the chat list.'}), 500


@chat_bp.route('/create-chat', methods=['POST'])
def create_chat_route():
    """
    Create a new chat between the logged-in user and a selected contact.
    Expects JSON payload: {"contact_id": <contact_id>}
    """
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)

        # Get the contact_id from the request payload
        data = request.get_json()
        contact_id = data.get('contact_id')

        if not contact_id:
            return jsonify({'error': 'Missing contact_id in request.'}), 400

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Call the model function to create the chat
    try:
        success = create_chat(user_id, contact_id)
        if not success:
            return jsonify({'error': 'Failed to create chat.'}), 500

        return jsonify({'message': 'Chat created successfully.'}), 201

    except Exception as e:
        print(f"Error creating chat: {e}")
        return jsonify({'error': 'An error occurred while creating the chat.'}), 500