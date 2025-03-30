# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from oqs import KeyEncapsulation

# Initialize Kyber for key exchange
kem = KeyEncapsulation("Kyber512")

def encrypt_data(key, plaintext):
    # Generate a random 16-byte IV
    iv = os.urandom(16)

    # Pad the plaintext using PKCS7
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext.encode()) + padder.finalize()

    print("Plaintext:", plaintext)
    print("Padded plaintext:", padded_plaintext)

    # Encrypt the padded plaintext
    cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    print("Ciphertext:", iv + ciphertext)

    # Prepend the IV to the ciphertext
    return iv + ciphertext

def decrypt_data(key, ciphertext):
    try:
        # Extract the IV and actual ciphertext
        iv = ciphertext[:16]
        actual_ciphertext = ciphertext[16:]

        print("IV:", iv)
        print("Actual ciphertext:", actual_ciphertext)

        # Decrypt the ciphertext
        cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()

        print("Padded plaintext:", padded_plaintext)

        # Unpad the plaintext using PKCS7
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        print("Decrypted plaintext:", plaintext)

        # Decode the plaintext to a string
        return plaintext.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None