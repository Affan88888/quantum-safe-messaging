from oqs import KeyEncapsulation

# Initialize KEM
kem = KeyEncapsulation("Kyber512")

# Generate keypair
public_key = kem.generate_keypair()

# Encapsulate secret
ciphertext, encapsulated_key = kem.encap_secret(public_key)

# Decapsulate secret
shared_secret = kem.decap_secret(encapsulated_key)

print("Ciphertext:", ciphertext)
print("Encapsulated key:", encapsulated_key)
print("Shared secret:", shared_secret)