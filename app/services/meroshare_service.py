from app.internal.encrypt import encrypt_string, decrypt_string
from sqlalchemy.orm import Session

class MeroshareService:
    def __init__(self, db: Session, key: str = None):
        self.db = db
        self.key = key

    # Encryption methods
    def encrypt_username(self, username: str) -> str:
        return encrypt_string(username, self.key)
    
    def encrypt_password(self, password: str) -> str:
        return encrypt_string(password, self.key)

    def encrypt_crn(self, crn: str) -> str:
        return encrypt_string(crn, self.key)
    
    def encrypt_pin(self, pin: str) -> str:
        return encrypt_string(pin, self.key)
    
    # Decryption methods
    def decrypt_username(self, encrypted_username: str, ):
        return decrypt_string(encrypted_username, self.key)
    
    def decrypt_password(self, encrypted_password: str):
        return decrypt_string(encrypted_password, self.key)
    
    def decrypt_crn(self, encrypted_crn: str):
        return decrypt_string(encrypted_crn, self.key)
    
    def decrypt_pin(self, encrypted_pin: str):
        return decrypt_string(encrypted_pin, self.key)
