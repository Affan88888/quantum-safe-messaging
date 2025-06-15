import oqs
from unittest import TestCase

class TestKyber(TestCase):
    def test_kyber_key_exchange(self):
        kemalg = "Kyber512"  # Or "ML-KEM-512"

        with oqs.KeyEncapsulation(kemalg) as client_kem:
            public_key = client_kem.generate_keypair()

            # Server side: encapsulate
            ciphertext, shared_secret_server = client_kem.encap_secret(public_key)

            # Client side: decapsulate
            shared_secret_client = client_kem.decap_secret(ciphertext)

            self.assertEqual(shared_secret_client, shared_secret_server)

    def test_kyber_decapsulate_with_wrong_key(self):
        kemalg = "Kyber512"

        with oqs.KeyEncapsulation(kemalg) as client_kem:
            public_key = client_kem.generate_keypair()
            ciphertext, _ = client_kem.encap_secret(public_key)

        # Use a different instance with its own key
        with oqs.KeyEncapsulation(kemalg) as another_kem:
            another_public_key = another_kem.generate_keypair()
            ciphertext2, _ = another_kem.encap_secret(another_public_key)

            # Try to decapsulate with wrong key
            shared_secret_wrong = another_kem.decap_secret(ciphertext)

        # Shared secrets should NOT match
        shared_secret_correct = client_kem.decap_secret(ciphertext)
        self.assertNotEqual(shared_secret_wrong, shared_secret_correct)