import os
import base64
from unittest import TestCase
from utils.helpers import encrypt_data, decrypt_data  # Make sure path matches your structure

class TestEncryption(TestCase):

    def test_encrypt_decrypt(self):
        # Simulate shared secret (32 bytes for Kyber-derived key)
        shared_secret = os.urandom(32)  # Use real derived key in production

        plaintext = "Secret quantum message."

        # Encrypt
        encrypted_blob = encrypt_data(shared_secret, plaintext)

        # Decrypt
        decrypted = decrypt_data(shared_secret, encrypted_blob)

        # Assert
        self.assertEqual(plaintext, decrypted)

    def test_decryption_fails_with_wrong_key(self):
        shared_secret = os.urandom(32)
        wrong_key = os.urandom(32)
        plaintext = "Top secret quantum message"

        encrypted_blob = encrypt_data(shared_secret, plaintext)
        decrypted = decrypt_data(wrong_key, encrypted_blob)

        self.assertIsNone(decrypted)

    def test_encrypt_empty_message(self):
        shared_secret = os.urandom(32)
        plaintext = ""

        encrypted_blob = encrypt_data(shared_secret, plaintext)
        decrypted = decrypt_data(shared_secret, encrypted_blob)

        self.assertEqual(plaintext, decrypted)

    def test_corrupted_ciphertext(self):
        shared_secret = os.urandom(32)
        plaintext = "Important message"

        encrypted_blob = encrypt_data(shared_secret, plaintext)
        corrupted_blob = bytearray(encrypted_blob)
        if len(corrupted_blob) > 0:
            corrupted_blob[0] ^= 0xFF  # Flip a byte

        decrypted = decrypt_data(shared_secret, bytes(corrupted_blob))
        self.assertIsNone(decrypted)

    def test_repeated_encrypt_decrypt(self):
        shared_secret = os.urandom(32)
        plaintext = "Repeatable test message"

        for _ in range(5):  # Repeat multiple times
            encrypted_blob = encrypt_data(shared_secret, plaintext)
            decrypted = decrypt_data(shared_secret, encrypted_blob)
            self.assertEqual(plaintext, decrypted)