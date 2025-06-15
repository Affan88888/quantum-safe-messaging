# tests/test_crypto_utils.py

import unittest
import os
from utils.helpers import derive_key, encrypt_data, decrypt_data, encrypt_session, decrypt_session
import base64
import oqs


class TestCryptoUtils(unittest.TestCase):

    def setUp(self):
        """Set up shared secrets and keys"""
        self.shared_secret = os.urandom(32)  # Simulated shared secret
        self.plaintext = "Secret message goes here."
        self.kemalg = "ML-KEM-512"

        # Generate Kyber keypair for session tests
        with oqs.KeyEncapsulation(self.kemalg) as client_kem:
            self.public_key_client = client_kem.generate_keypair()
            self.private_key_client = client_kem.export_secret_key()

    def test_01_derive_key(self):
        """Test HKDF-based key derivation"""
        derived = derive_key(self.shared_secret)
        self.assertEqual(len(derived), 32, "Derived key must be 32 bytes")

    def test_02_aes_gcm_encrypt_decrypt(self):
        """Test AES-GCM encryption and decryption"""
        key = derive_key(self.shared_secret)
        encrypted = encrypt_data(key, self.plaintext)
        decrypted = decrypt_data(key, encrypted)

        self.assertEqual(decrypted, self.plaintext, "Decrypted text should match original plaintext")

    def test_03_invalid_decryption(self):
        """Test that invalid decryption fails gracefully"""
        key = derive_key(self.shared_secret)
        encrypted = encrypt_data(key, self.plaintext)

        # Corrupt ciphertext
        corrupted = encrypted[:-5] + b'corrupt'

        result = decrypt_data(key, corrupted)
        self.assertIsNone(result, "Corrupted data should not decrypt")

    def test_04_kyber_encap_decap(self):
        """Test Kyber encapsulation and decapsulation"""
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as server_kem:
            ciphertext, shared_secret_server = server_kem.encap_secret(self.public_key_client)

        with oqs.KeyEncapsulation(kemalg, self.private_key_client) as client_kem:
            shared_secret_client = client_kem.decap_secret(ciphertext)

        self.assertEqual(shared_secret_server, shared_secret_client, "Shared secrets should match")

    def test_05_encrypt_session(self):
        """Test session encryption with Kyber"""
        user_id = 1234
        session_data = encrypt_session(user_id, self.public_key_client)

        self.assertIn('encrypted_session_data', session_data)
        self.assertIn('encapsulated_key', session_data)

    def test_06_decrypt_session(self):
        """Test session decryption with private key"""
        user_id = 1234
        session_data = encrypt_session(user_id, self.public_key_client)

        session_dict = {
            'encrypted_session_data': session_data['encrypted_session_data'],
            'encapsulated_key': session_data['encapsulated_key'],
            'private_key': base64.b64encode(self.private_key_client).decode()
        }

        decrypted_user_id = decrypt_session(session_dict)
        self.assertEqual(decrypted_user_id, str(user_id))

    def test_07_decrypt_session_with_missing_fields(self):
        """Test that missing fields raise ValueError"""
        with self.assertRaises(ValueError):
            decrypt_session({})  # Empty dict should fail

    def test_08_encrypt_session_invalid_public_key(self):
        """Test failure when public key is invalid"""
        with self.assertRaises(Exception):
            encrypt_session(1234, b"invalid-public-key")


if __name__ == '__main__':
    unittest.main()
    