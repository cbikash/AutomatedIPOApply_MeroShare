
from pydantic import BaseModel,field_validator, computed_field
from app.internal.encrypt import encrypt_string, decrypt_string
from app.schemas.user import UserRead

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


class MeroshareRead(MeroshareBase):
    username : str 
    password: str
    client_id: str
    crn: str
    pin: str
    user_id: int
    user: UserRead

    class Config:
        from_attributes = True
    
    @computed_field
    def decrypted_username(self) -> str:
        return decrypt_string(self.username, key=self.user.key)
    
    @computed_field
    def decrypted_password(self) -> str:
        return decrypt_string(self.password, key=self.user.key)
    
    @computed_field
    def decrypted_crn(self) -> str:
        return decrypt_string(self.crn, key=self.user.key)
    
    @computed_field
    def decrypted_pin(self) -> str:
        return decrypt_string(self.pin, key=self.user.key)
    

    





