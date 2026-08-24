import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def calculate_file_hash_from_bytes(file_bytes: bytes) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(file_bytes)
    return sha256_hash.hexdigest()

def encrypt_code(code_text: str, password: str) -> tuple[bytes, str]:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    
    encrypted_data = f.encrypt(code_text.encode())
    payload = salt + encrypted_data
    file_hash = calculate_file_hash_from_bytes(payload)
    return payload, file_hash

def decrypt_code(file_bytes: bytes, password: str) -> str:
    if len(file_bytes) < 16:
        raise ValueError("Invalid file structure: File is too short or corrupted.")
        
    salt = file_bytes[:16]
    encrypted_data = file_bytes[16:]
    
    key = derive_key(password, salt)
    f = Fernet(key)
    
    try:
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data.decode()
    except InvalidToken:
        raise ValueError("Authentication Failed: Incorrect password or tampered file.")