def rot13(text):
    result = []

    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(char)

    return ''.join(result)


# Encryption
plaintext = "Hello, World!"
ciphertext = rot13(plaintext)
print("Encrypted:", ciphertext)

# Decryption
decrypted = rot13(ciphertext)
print("Decrypted:", decrypted)
