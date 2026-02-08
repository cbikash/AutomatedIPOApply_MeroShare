
from pydantic import BaseModel,field_validator, computed_field
from app.internal.encrypt import encrypt_string, decrypt_string

class MeroshareBase(BaseModel):

    username : str 
    password: str
    client_id: str
    crn: str
    pin: int
    user_id: int


class MeroshareCreate(MeroshareBase):
    username : str 
    password: str
    client_id: str
    crn: str
    pin: int
    user_id: int

    @field_validator("username")
    @classmethod
    def encrypt_username(cls, v: str) -> str:
        return encrypt_string(v)

    @field_validator("password")
    @classmethod
    def encrypt_password(cls, v: str)-> str:
        return encrypt_string(v)
    
    @field_validator("crn")
    @classmethod
    def encrypt_crn(cls, v:str)-> str:
        return encrypt_string(v)
    
    @field_validator('pin')
    @classmethod
    def encrypt_pin(cls, v:str) -> str:
        return encrypt_string(v)


class MeroshareRead(MeroshareBase):
    username : str 
    password: str
    client_id: str
    crn: str
    pin: str
    user_id: int

    @computed_field
    @property
    def decrypted_username(self) -> str:
        return decrypt_string(self.username)
    
    @computed_field
    @property
    def decrypted_password(self) -> str:
        return decrypt_string(self.password)
    
    @computed_field
    @property
    def decrypted_pin(self) -> str:
        return decrypt_string(self.pin)
    
    @computed_field
    @property
    def decrypted_crn(self) -> str:
        return decrypt_string(self.crn)





