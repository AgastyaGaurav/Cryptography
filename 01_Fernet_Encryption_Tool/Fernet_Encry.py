from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"


def generate_key():
    """Generate and save a new Fernet key."""
    key = Fernet.generate_key()

    with open(KEY_FILE, "wb") as f:
        f.write(key)

    print("Key generated and saved as", KEY_FILE)


def load_key():
    """Load the Fernet key from file."""
    if not os.path.exists(KEY_FILE):
        print("Key file not found.")
        print("Please generate a key first.")
        return None

    with open(KEY_FILE, "rb") as f:
        return f.read()


def encrypt_message():
    key = load_key()
    if key is None:
        return

    cipher = Fernet(key)

    message = input("Enter message to encrypt: ")

    encrypted = cipher.encrypt(message.encode())

    print("\nEncrypted Message:\n")
    print(encrypted.decode())


def decrypt_message():
    key = load_key()
    if key is None:
        return

    cipher = Fernet(key)

    encrypted = input("Enter encrypted message: ")

    try:
        decrypted = cipher.decrypt(encrypted.encode())

        print("\nDecrypted Message:\n")
        print(decrypted.decode())

    except Exception:
        print("Invalid key or encrypted message.")


def menu():
    while True:
        print("\n====== Fernet Encryption Tool ======")
        print("1. Generate Key")
        print("2. Encrypt Message")
        print("3. Decrypt Message")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            generate_key()

        elif choice == "2":
            encrypt_message()

        elif choice == "3":
            decrypt_message()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
