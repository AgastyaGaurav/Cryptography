# Simple Caesar Cipher in Python

def encrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            # Preserve uppercase/lowercase
            start = ord('A') if char.isupper() else ord('a')

            # Shift character
            encrypted_char = chr((ord(char) - start + shift) % 26 + start)
            result += encrypted_char
        else:
            result += char

    return result


def decrypt(text, shift):
    return encrypt(text, -shift)


# Example usage
message = "Hello World"
shift_value = 3

encrypted = encrypt(message, shift_value)
decrypted = decrypt(encrypted, shift_value)

print("Original :", message)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)
