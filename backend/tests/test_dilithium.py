import oqs
from unittest import TestCase

class TestDilithium(TestCase):
    def test_sign_verify(self):
        sigalg = "Dilithium2"

        # Create signer instance
        with oqs.Signature(sigalg) as signer:
            # Generate keypair manually
            public_key = signer.generate_keypair()

            # Sign a message
            message = b"Hello, quantum world!"
            signature = signer.sign(message)

            # Verify the signature
            is_valid = signer.verify(message, signature, public_key)

            self.assertTrue(is_valid)

    def test_invalid_signature_on_tampered_message(self):
        sigalg = "Dilithium2"

        with oqs.Signature(sigalg) as signer:
            # Generate keypair
            public_key = signer.generate_keypair()

            # Sign original message
            message = b"Original message"
            signature = signer.sign(message)

            # Tamper with the message
            tampered_message = b"Modified message"

            # Try to verify with tampered message
            is_valid = signer.verify(tampered_message, signature, public_key)

            # Should fail
            self.assertFalse(is_valid)