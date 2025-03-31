# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
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