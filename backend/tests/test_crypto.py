import unittest
from utils.helpers import derive_key, encrypt_data, decrypt_data
import oqs

class TestCryptoFunctions(unittest.TestCase):

    def test_kyber_key_encapsulation(self):
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg) as client:
            public_key = client.generate_keypair()
            ciphertext, shared_secret_server = client.encap_secret(public_key)
            self.assertEqual(len(shared_secret_server), 32)

    def test_derive_key(self):
        secret = b"shared-secret-test"
        key = derive_key(secret)
        self.assertEqual(len(key), 32)

    def test_encrypt_decrypt(self):
        secret = b"shared-secret-test"
        derived_key = derive_key(secret)
        plaintext = "Hello quantum world!"
        encrypted = encrypt_data(derived_key, plaintext)
        decrypted = decrypt_data(derived_key, encrypted)
        self.assertEqual(decrypted, plaintext)

if __name__ == '__main__':
    unittest.main()
    