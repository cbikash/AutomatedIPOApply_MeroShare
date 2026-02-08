from cryptography.fernet import Fernet
from app.core.setting import settings

FERNET_KEY = settings.ENCRYPTION_KEY

if not FERNET_KEY:
    raise RuntimeError("Encryption key not set")


fernet = Fernet(FERNET_KEY.encode())

def encrypt_string(value: str) -> str:
    return fernet.encrypt(str(value).encode("utf-8")).decode("utf-8")

def decrypt_string(value: str) -> str:
    return fernet.decrypt(value.encode("utf-8")).decode("utf-8")