from flask import Blueprint, request, jsonify, session
from models.user_theme_model import update_user_theme
from utils.helpers import decrypt_session

theme_bp = Blueprint('theme', __name__)

@theme_bp.route('/update-theme', methods=['POST'])
def update_theme():
    """
    Update the theme preference (light/dark) for the authenticated user.
    Expects a JSON payload with the 'theme' field ('light' or 'dark').
    """
    try:
        # Decrypt session data to get user_id
        user_id = decrypt_session(session)
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    # Extract the theme from the JSON payload
    data = request.json
    theme = data.get('theme')

    # Validate the theme value
    if theme not in ['light', 'dark']:
        return jsonify({'error': 'Invalid theme value. Must be "light" or "dark".'}), 400

    # Update the user's theme in the database
    try:
        if update_user_theme(user_id, theme):
            return jsonify({'message': 'Theme updated successfully', 'theme': theme}), 200
        else:
            return jsonify({'error': 'Failed to update theme'}), 500
    except Exception as e:
        print(f"Error updating theme: {e}")
        return jsonify({'error': 'An error occurred while updating the theme.'}), 500