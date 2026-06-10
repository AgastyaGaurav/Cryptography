def rail_fence_encrypt(text, rails):
    rail = ['' for _ in range(rails)]

    row = 0
    direction = 1

    for ch in text:
        rail[row] += ch

        if row == 0:
            direction = 1
        elif row == rails - 1:
            direction = -1

        row += direction

    return ''.join(rail)


text = input("Enter plaintext: ")
rails = int(input("Enter number of rails: "))

ciphertext = rail_fence_encrypt(text, rails)

print("Encrypted Text:", ciphertext)
