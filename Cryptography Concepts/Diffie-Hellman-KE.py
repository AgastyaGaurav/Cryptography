# Diffie-Hellman Key Exchange

import random

# Publicly shared prime number and primitive root
p = 23      # Prime number
g = 5       # Primitive root modulo p

print("Publicly Shared Values:")
print("Prime (p):", p)
print("Primitive Root (g):", g)

# Alice's private key
alice_private = random.randint(1, p - 2)
alice_public = pow(g, alice_private, p)

# Bob's private key
bob_private = random.randint(1, p - 2)
bob_public = pow(g, bob_private, p)

print("\nAlice:")
print("Private Key:", alice_private)
print("Public Key:", alice_public)

print("\nBob:")
print("Private Key:", bob_private)
print("Public Key:", bob_public)

# Exchange public keys and compute shared secret
alice_shared_secret = pow(bob_public, alice_private, p)
bob_shared_secret = pow(alice_public, bob_private, p)

print("\nShared Secret Computed by Alice:", alice_shared_secret)
print("Shared Secret Computed by Bob:", bob_shared_secret)

if alice_shared_secret == bob_shared_secret:
    print("\nKey Exchange Successful!")
else:
    print("\nKey Exchange Failed!")
