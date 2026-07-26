from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Generate a valid 24-byte 3DES key
while True:
    try:
        key = DES3.adjust_key_parity(get_random_bytes(24))
        break
    except ValueError:
        pass

# Generate an 8-byte IV
iv = get_random_bytes(8)

# Create cipher (CBC mode)
cipher = DES3.new(key, DES3.MODE_CBC, iv)

plaintext = b"Hello, Triple DES!"

# Encrypt
ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))

print("Ciphertext:", ciphertext.hex())

# Decrypt
decipher = DES3.new(key, DES3.MODE_CBC, iv)
decrypted = unpad(decipher.decrypt(ciphertext), DES3.block_size)

print("Decrypted:", decrypted.decode())
