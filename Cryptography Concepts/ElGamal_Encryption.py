import random

# Function to find modular inverse
def mod_inverse(a, p):
    return pow(a, -1, p)

# Key Generation
def generate_keys():
    p = 467  # A prime number
    g = 2    # Primitive root modulo p

    x = random.randint(2, p - 2)   # Private key
    y = pow(g, x, p)               # Public key

    return (p, g, y), x

# Encryption
def encrypt(public_key, message):
    p, g, y = public_key

    k = random.randint(2, p - 2)   # Random ephemeral key

    c1 = pow(g, k, p)
    s = pow(y, k, p)               # Shared secret
    c2 = (message * s) % p

    return (c1, c2)

# Decryption
def decrypt(private_key, public_key, ciphertext):
    p, g, y = public_key
    c1, c2 = ciphertext

    s = pow(c1, private_key, p)
    s_inv = mod_inverse(s, p)

    message = (c2 * s_inv) % p
    return message

# Driver Code
if __name__ == "__main__":
    public_key, private_key = generate_keys()

    print("Public Key:", public_key)
    print("Private Key:", private_key)

    message = int(input("Enter message (integer less than p): "))

    if message >= public_key[0]:
        print("Message must be less than", public_key[0])
    else:
        ciphertext = encrypt(public_key, message)
        print("Encrypted Ciphertext:", ciphertext)

        decrypted_message = decrypt(private_key, public_key, ciphertext)
        print("Decrypted Message:", decrypted_message)
