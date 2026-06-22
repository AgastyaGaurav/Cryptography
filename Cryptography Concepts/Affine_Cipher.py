def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def encrypt(plaintext, a, b):
    ciphertext = ""

    for ch in plaintext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            x = ord(ch) - base
            encrypted = chr(((a * x + b) % 26) + base)
            ciphertext += encrypted
        else:
            ciphertext += ch

    return ciphertext


def decrypt(ciphertext, a, b):
    a_inv = mod_inverse(a, 26)

    if a_inv is None:
        return "Invalid key: 'a' has no modular inverse modulo 26."

    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            y = ord(ch) - base
            decrypted = chr((a_inv * (y - b)) % 26 + base)
            plaintext += decrypted
        else:
            plaintext += ch

    return plaintext


# Main Program
text = input("Enter message: ")
a = int(input("Enter key a (must be coprime with 26): "))
b = int(input("Enter key b: "))

encrypted = encrypt(text, a, b)
print("\nEncrypted Text:", encrypted)

decrypted = decrypt(encrypted, a, b)
print("Decrypted Text:", decrypted)
