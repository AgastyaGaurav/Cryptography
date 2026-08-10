
"""
Secure Password Hashing System
Uses Argon2id for password storage.

Install:
    pip install argon2-cffi
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError


# Argon2id password hasher
ph = PasswordHasher(
    time_cost=3,
    memory_cost=65536,   # 64 MB
    parallelism=4,
    hash_len=32,
    salt_len=16
)


def hash_password(password: str) -> str:
    """
    Generate a secure Argon2id password hash.
    """
    return ph.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against an existing hash.
    """
    try:
        return ph.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


def main():
    print("=== Secure Password System ===")

    password = input("Enter password: ")

    password_hash = hash_password(password)

    print("\nStored password hash:")
    print(password_hash)

    test_password = input("\nEnter password to verify: ")

    if verify_password(test_password, password_hash):
        print("[PASS] Password is correct.")
    else:
        print("[FAIL] Invalid password.")


if __name__ == "__main__":
    main()
