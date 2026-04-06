
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


class MeroshareRead(MeroshareBase):
    username : str 
    password: str
    client_id: str
    crn: str
    pin: str
    user_id: int

    





