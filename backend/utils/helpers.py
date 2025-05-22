# utils/helpers.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
import base64
import oqs
import os

# 🔐 Use HKDF to derive cryptographically secure keys
def derive_key(shared_secret):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'kyber-session-key',
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

# 🛡️ AES-GCM for authenticated encryption
def encrypt_data(key, plaintext):
    # Generate a random 12-byte nonce for GCM
    nonce = os.urandom(12)
    
    # Derive key via HKDF
    derived_key = derive_key(key)
    
    encryptor = Cipher(
        algorithms.AES(derived_key),
        modes.GCM(nonce),
        backend=default_backend()
    ).encryptor()
    
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return nonce + encryptor.tag + ciphertext  # Include nonce and tag

def decrypt_data(key, ciphertext):
    try:
        # Extract components
        nonce = ciphertext[:12]
        tag = ciphertext[12:28]
        encrypted_data = ciphertext[28:]
        
        # Derive key via HKDF
        derived_key = derive_key(key)
        
        decryptor = Cipher(
            algorithms.AES(derived_key),
            modes.GCM(nonce, tag),
            backend=default_backend()
        ).decryptor()
        
        plaintext = decryptor.update(encrypted_data) + decryptor.finalize()
        return plaintext.decode()
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None

# 🔐 Post-Quantum Session Encryption
def encrypt_session(user_id, public_key_client):
    kemalg = "ML-KEM-512"
    with oqs.KeyEncapsulation(kemalg) as server:
        ciphertext, shared_secret = server.encap_secret(public_key_client)
    
    session_key = derive_key(shared_secret)
    encrypted_data = encrypt_data(session_key, str(user_id))
    
    return {
        'encrypted_session_data': base64.b64encode(encrypted_data).decode(),
        'encapsulated_key': base64.b64encode(ciphertext).decode()
    }

def decrypt_session(session):
    encrypted_session_data = session.get('encrypted_session_data')
    encapsulated_key = session.get('encapsulated_key')
    private_key = session.get('private_key')

    if not all([encrypted_session_data, encapsulated_key, private_key]):
        raise ValueError('User not authenticated')

    try:
        # Decode Base64
        encrypted_session_data = base64.b64decode(encrypted_session_data)
        encapsulated_key = base64.b64decode(encapsulated_key)
        private_key = base64.b64decode(private_key)

        # Decapsulate shared secret
        kemalg = "ML-KEM-512"
        with oqs.KeyEncapsulation(kemalg, private_key) as client:
            shared_secret = client.decap_secret(encapsulated_key)

        session_key = derive_key(shared_secret)
        user_id = decrypt_data(session_key, encrypted_session_data)
        return user_id
    except Exception as e:
        print(f"Error validating session: {e}")
        raise ValueError('Invalid session or authentication failed')