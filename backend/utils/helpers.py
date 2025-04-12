# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import oqs
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