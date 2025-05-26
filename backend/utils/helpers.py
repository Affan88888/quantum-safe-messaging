# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import oqs
from oqs import KeyEncapsulation
import os

def encrypt_data(key, plaintext):
    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Pad the plaintext using PKCS7
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    # Encrypt the padded plaintext
    cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    # Prepend the IV to the ciphertext
    return iv + ciphertext

def decrypt_data(key, ciphertext):
    try:
        # Extract the IV and actual ciphertext
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        # Decrypt the ciphertext
        cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        # Unpad the plaintext using PKCS7
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        # Decode the plaintext to a string
        return plaintext.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

def encrypt_session(user_id, public_key_client):
    """
    Encrypts session data using quantum-safe shared secret generation.

    Args:
        user_id (str): The ID of the user to be encrypted.
        public_key_client (bytes): The client's public key for shared secret generation.

    Returns:
        dict: Encrypted session data including ciphertext, private key, and encrypted user ID.
    """
    # Simulate the server encapsulating the shared secret
    kemalg = "ML-KEM-512"
    with oqs.KeyEncapsulation(kemalg) as server:
        ciphertext, shared_secret_server = server.encap_secret(public_key_client)

    # Use the shared secret as the session key
    session_key = shared_secret_server[:32]

    # Encrypt the user ID using the session key
    encrypted_session_data = encrypt_data(session_key, str(user_id))

    # Return the encrypted session data
    return {
        'encrypted_session_data': base64.b64encode(encrypted_session_data).decode('utf-8'),
        'encapsulated_key': base64.b64encode(ciphertext).decode('utf-8')
    }

def decrypt_session(session):
    """
    Decrypts the session data to retrieve the user_id.
    Returns the user_id if successful, otherwise raises an exception.
    """
    # Step 1: Retrieve session data
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')
    private_key = session.get('private_key')

    # Ensure all required session data is present
    if not all([encrypted_session_data, encapsulated_key, private_key]):
        raise ValueError('User not authenticated')

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

        return user_id

    except Exception as e:
        print(f"Error validating session: {e}")
        raise ValueError('Invalid session or authentication failed')
    
def encrypt_message(message, recipient_public_key):
    """
    Encrypts a message using the recipient's public key and quantum-safe shared secret generation.

    Args:
        message (str): The plaintext message to be encrypted.
        recipient_public_key (bytes): The recipient's public key for encryption.

    Returns:
        dict: Encrypted message data including ciphertext and encapsulated key.
    """
    # Simulate the sender encapsulating the shared secret
    kemalg = "ML-KEM-512"
    with KeyEncapsulation(kemalg) as sender:
        encapsulated_key, shared_secret_sender = sender.encap_secret(recipient_public_key)

    # Use the shared secret as the message encryption key
    message_key = shared_secret_sender[:32]
    #print("Shared Secret (Encryption):", message_key)

    # Encrypt the message using the message key
    encrypted_message = encrypt_data(message_key, message)

    # Return the encrypted message data
    return {
        'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
        'encapsulated_key': base64.b64encode(encapsulated_key).decode('utf-8')
    }

def decrypt_message(encrypted_message_data, private_key_message):
    """
    Decrypts an encrypted message using the recipient's private key and encapsulated key.

    Args:
        encrypted_message_data (dict): A dictionary containing the encrypted message and encapsulated key.
        private_key_message (bytes): The recipient's private key for decryption.

    Returns:
        str: The decrypted plaintext message.
    """
    # Step 1: Retrieve encrypted message data
    encrypted_message = encrypted_message_data.get('encrypted_message')
    encapsulated_key = encrypted_message_data.get('encapsulated_key')

    # Ensure all required data is present
    if not all([encrypted_message, encapsulated_key, private_key_message]):
        raise ValueError('Missing required data for decryption')

    try:
        # Step 2: Decode Base64-encoded data
        encrypted_message = base64.b64decode(encrypted_message)
        encapsulated_key = base64.b64decode(encapsulated_key)

        # Step 3: Decapsulate the shared secret
        kemalg = "ML-KEM-512"
        with KeyEncapsulation(kemalg, private_key_message) as recipient:
            shared_secret = recipient.decap_secret(encapsulated_key)

        # Step 4: Derive the message key
        message_key = shared_secret[:32]

        # Step 5: Decrypt the message using the full encrypted_message
        decrypted_message = decrypt_data(message_key, encrypted_message)

        return decrypted_message

    except Exception as e:
        print(f"Error decrypting message: {e}")
        raise ValueError('Invalid message or decryption failed')