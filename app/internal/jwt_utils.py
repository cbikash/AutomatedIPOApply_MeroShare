from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from app.core.setting import Settings
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password): #verify password using pwdlib
    return password_hasher.verify(plain_password, hashed_password)


def get_password_hash(password): #hash password using pwdlib
    return password_hasher.hash(password)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
