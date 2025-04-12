from flask import Blueprint, request, jsonify, session
from models.user_model import get_user_by_email
from models.contact_model import add_contact_to_user, get_contacts_for_user
from utils.helpers import decrypt_data
import oqs
import base64

# Create a Blueprint for contact-related routes
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/check-email', methods=['POST'])
def check_email():
    """
    Check if the provided email exists in the users table.
    If it exists, add the email as a contact for the logged-in user.
    """
    # Step 1: Retrieve session data
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')
    private_key = session.get('private_key')

    # Ensure all required session data is present
    if not all([encrypted_session_data, encapsulated_key, private_key]):
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        # Step 2: Decode Base64-encoded session data
        encrypted_session_data = base64.b64decode(encrypted_session_data)
        encapsulated_key = base64.b64decode(encapsulated_key)

        # Step 3: Decapsulate the shared secret
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg, private_key) as client:
            shared_secret = client.decap_secret(encapsulated_key)

        # Step 4: Derive the session key
        session_key = shared_secret[:32]

        # Step 5: Decrypt the session data
        user_id = decrypt_data(session_key, encrypted_session_data)

    except Exception as e:
        print(f"Error validating session: {e}")
        return jsonify({'error': 'Invalid session or authentication failed'}), 401

    # Step 6: Process the email check logic
    data = request.json
    email_to_check = data.get('email')

    if not email_to_check:
        return jsonify({'error': 'Email is required'}), 400

    # Check if the email exists in the database
    user_to_add = get_user_by_email(email_to_check)
    if not user_to_add:
        return jsonify({'exists': False, 'message': 'User with this email does not exist.'}), 404

    # Add the email as a contact for the logged-in user
    try:
        success = add_contact_to_user(user_id, user_to_add['id'])
        if success:
            return jsonify({
                'exists': True,
                'message': 'Contact added successfully.',
                'contact': {
                    'id': user_to_add['id'],
                    'username': user_to_add['username'],
                    'email': user_to_add['email']
                }
            }), 200
        else:
            return jsonify({'error': 'Failed to add contact.'}), 500
    except Exception as e:
        print(f"Error adding contact: {e}")
        return jsonify({'error': 'An error occurred while adding the contact.'}), 500
    

@contact_bp.route('/get-contact-list', methods=['GET'])
def get_contact_list():
    """
    Retrieve the list of contacts for the logged-in user.
    """
    # Step 1: Retrieve session data
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')
    private_key = session.get('private_key')

    # Ensure all required session data is present
    if not all([encrypted_session_data, encapsulated_key, private_key]):
        return jsonify({'error': 'User not authenticated'}), 401

    try:
        # Step 2: Decode Base64-encoded session data
        encrypted_session_data = base64.b64decode(encrypted_session_data)
        encapsulated_key = base64.b64decode(encapsulated_key)

        # Step 3: Decapsulate the shared secret
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg, private_key) as client:
            shared_secret = client.decap_secret(encapsulated_key)

        # Step 4: Derive the session key
        session_key = shared_secret[:32]

        # Step 5: Decrypt the session data
        user_id = decrypt_data(session_key, encrypted_session_data)

    except Exception as e:
        print(f"Error validating session: {e}")
        return jsonify({'error': 'Invalid session or authentication failed'}), 401

    # Step 6: Fetch the contact list for the user
    try:
        contacts = get_contacts_for_user(user_id)
        if not contacts:
            return jsonify({'message': 'No contacts found.', 'contacts': []}), 200

        return jsonify({
            'message': 'Contacts retrieved successfully.',
            'contacts': contacts
        }), 200

    except Exception as e:
        print(f"Error fetching contact list: {e}")
        return jsonify({'error': 'An error occurred while fetching the contact list.'}), 500