"""
Secure Password Generator + Argon2id Password Hashing

Install:
    pip install argon2-cffi
"""

import secrets
import string

from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError,
)


# Argon2id password hasher
password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=65536,   # 64 MB
    parallelism=4,
    hash_len=32,
    salt_len=16
)


def generate_password(
    length=20,
    use_uppercase=True,
    use_lowercase=True,
    use_numbers=True,
    use_symbols=True
):
    """
    Generate a cryptographically secure random password.
    """

    if length < 8:
        raise ValueError(
            "Password length must be at least 8 characters."
        )

    character_sets = []

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_numbers:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append("!@#$%^&*()-_=+[]{};:,.?")

    if not character_sets:
        raise ValueError(
            "At least one character category must be enabled."
        )

    # Combine all allowed characters.
    all_characters = "".join(character_sets)

    # Guarantee at least one character from every
    # selected character category.
    password = [
        secrets.choice(characters)
        for characters in character_sets
    ]

    # Fill remaining length.
    while len(password) < length:
        password.append(
            secrets.choice(all_characters)
        )

    # Securely shuffle the generated password.
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def hash_password(password):
    """
    Hash a password using Argon2id.
    """

    return password_hasher.hash(password)


def verify_password(password, password_hash):
    """
    Verify a password against an Argon2id hash.
    """

    try:
        return password_hasher.verify(
            password_hash,
            password
        )

    except (
        VerifyMismatchError,
        VerificationError
    ):
        return False


def main():

    print("=" * 45)
    print(" Secure Password Generator")
    print("=" * 45)

    try:

        length = int(
            input(
                "\nPassword length [minimum 8]: "
            )
        )

        # Generate password.
        password = generate_password(
            length=length,
            use_uppercase=True,
            use_lowercase=True,
            use_numbers=True,
            use_symbols=True
        )

        print("\nGenerated password:")
        print(password)

        # Hash password.
        password_hash = hash_password(password)

        print("\nArgon2id password hash:")
        print(password_hash)

        # Verify generated password.
        if verify_password(
            password,
            password_hash
        ):
            print(
                "\n[PASS] Password verification successful."
            )
        else:
            print(
                "\n[FAIL] Password verification failed."
            )

        # Demonstrate incorrect password.
        wrong_password = "IncorrectPassword123!"

        if verify_password(
            wrong_password,
            password_hash
        ):
            print(
                "[WARNING] Unexpected verification success."
            )
        else:
            print(
                "[PASS] Incorrect password rejected."
            )

    except ValueError as error:

        print(f"\n[ERROR] {error}")


if __name__ == "__main__":
    main()
```
