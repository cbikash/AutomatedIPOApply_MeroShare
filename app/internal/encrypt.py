from cryptography.fernet import Fernet

def encrypt_string(value: str, key: str = None) -> str:
    fernet = Fernet(key.encode())
    return fernet.encrypt(str(value).encode("utf-8")).decode("utf-8")

def decrypt_string(value: str, key: str = None) -> str:
    fernet = Fernet(key.encode())
    return fernet.decrypt(value.encode("utf-8")).decode("utf-8")

def generate_encryption_key() -> str:
    return Fernet.generate_key().decode("utf-8")