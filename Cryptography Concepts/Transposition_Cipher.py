import math

def encrypt(message, key):
    cipher = [''] * key

    for col in range(key):
        pointer = col

        while pointer < len(message):
            cipher[col] += message[pointer]
            pointer += key

    return ''.join(cipher)


def decrypt(ciphertext, key):
    num_cols = math.ceil(len(ciphertext) / key)
    num_rows = key
    num_shaded_boxes = (num_cols * num_rows) - len(ciphertext)

    plaintext = [''] * num_cols

    col = 0
    row = 0

    for symbol in ciphertext:
        plaintext[col] += symbol
        col += 1

        if (col == num_cols) or (
            col == num_cols - 1 and row >= num_rows - num_shaded_boxes
        ):
            col = 0
            row += 1

    return ''.join(plaintext)


# Driver code
message = input("Enter message: ")
key = int(input("Enter key: "))

encrypted = encrypt(message, key)
print("Encrypted Text:", encrypted)

decrypted = decrypt(encrypted, key)
print("Decrypted Text:", decrypted)
