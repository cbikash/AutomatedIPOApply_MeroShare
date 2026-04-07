from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    email: str
    name: str | None = None
    password: str | None = None
    disabled: bool | None = None


class UserCreate(UserBase):
    email: str
    name: str | None = None
    password: str | None = None
    disabled: bool | None = None

class UserRead(UserBase):
    id: int
    email: str
    name: str | None = None
    disabled: bool | None = None
    key: str | None = None

    class Config:
        from_attributes = True



