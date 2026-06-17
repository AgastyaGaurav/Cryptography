def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')

            if char.isupper():
                encrypted = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))

            ciphertext += encrypted
            key_index += 1
        else:
            ciphertext += char

    return ciphertext


def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key = key.upper()
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')

            if char.isupper():
                decrypted = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))

            plaintext += decrypted
            key_index += 1
        else:
            plaintext += char

    return plaintext


# Example usage
message = "HELLO WORLD"
key = "KEY"

encrypted = vigenere_encrypt(message, key)
print("Encrypted:", encrypted)

decrypted = vigenere_decrypt(encrypted, key)
print("Decrypted:", decrypted)
