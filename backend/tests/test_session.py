import unittest
from utils.helpers import encrypt_session, decrypt_session
import base64
import oqs

class TestSessionEncryption(unittest.TestCase):

    def test_encrypt_decrypt_session(self):
        kemalg = "ML-KEM-512"

        # Generate real Kyber keys for testing
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key = client.generate_keypair()
            private_key = client.export_secret_key()

        # Encrypt session
        encrypted_session = encrypt_session(1, public_key)

        # Prepare session data for decryption
        session_data = {
            'encrypted_session_data': encrypted_session['encrypted_session_data'],
            'encapsulated_key': encrypted_session['encapsulated_key'],
            'private_key': base64.b64encode(private_key).decode()
        }

        # Decrypt session
        user_id = decrypt_session(session_data)
        self.assertEqual(user_id, "1")

if __name__ == '__main__':
    unittest.main()