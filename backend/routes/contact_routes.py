from flask import Blueprint, request, jsonify, session
from models.user_model import get_user_by_email, get_user_by_id
from models.contact_model import add_contact_to_user, get_contacts_for_user, delete_contact
from utils.helpers import decrypt_session

# Create a Blueprint for contact-related routes
contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/check-email', methods=['POST'])
def check_email():
    """
    Check if the provided email exists in the users table.
    If it exists, add the email as a contact for the logged-in user.
    Prevent the user from adding their own email as a contact.
    """
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)

        # Fetch the logged-in user's details (including their email)
        logged_in_user = get_user_by_id(user_id)
        if not logged_in_user:
            return jsonify({'error': 'Failed to fetch logged-in user details.'}), 500

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Process the email check logic
    data = request.json
    email_to_check = data.get('email')

    if not email_to_check:
        return jsonify({'error': 'Email is required'}), 400

    # Check if the email belongs to the logged-in user
    if email_to_check == logged_in_user['email']:
        return jsonify({'exists': False, 'message': 'You cannot add yourself to your contacts.'}), 404

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
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Fetch the contact list for the user
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

@contact_bp.route('/delete-contact', methods=['DELETE'])
def delete_contact_route():
    """
    Delete a contact from the user's list of contacts.
    """
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Process the deletion logic
    data = request.json
    contact_id = data.get('contact_id')

    if not contact_id:
        return jsonify({'error': 'Contact ID is required'}), 400

    # Call the delete_contact function
    try:
        success = delete_contact(user_id, contact_id)
        if success:
            return jsonify({'message': 'Contact deleted successfully.'}), 200
        else:
            return jsonify({'error': 'Failed to delete contact or contact not found.'}), 404
    except Exception as e:
        print(f"Error deleting contact: {e}")
        return jsonify({'error': 'An error occurred while deleting the contact.'}), 500