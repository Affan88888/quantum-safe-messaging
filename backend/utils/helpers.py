# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from oqs import KeyEncapsulation

# Initialize Kyber for key exchange
kem = KeyEncapsulation("Kyber512")

def encrypt_data(key, plaintext):
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to match block size
    padded_plaintext = plaintext.encode() + b"\0" * (16 - len(plaintext) % 16)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

    return iv + ciphertext  # Prepend IV to ciphertext

def decrypt_data(key, ciphertext):
    iv = ciphertext[:16]
    actual_ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
    plaintext = padded_plaintext.rstrip(b"\0").decode()

    return plaintext