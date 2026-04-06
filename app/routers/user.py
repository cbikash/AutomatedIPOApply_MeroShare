from fastapi import APIRouter, Request, Depends
from app.schemas.user import UserCreate
from app.models.user import User
from sqlalchemy.orm import Session
from app.deps import get_db
from app.internal.jwt_utils import get_password_hash


router = APIRouter(prefix='/users')

@router.get("/")
def read_users(request: Request = None):
    ip = request.client.host
    return {"message": f"Hello, your IP address is {ip}"}

@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_dict = user.model_dump()
    password = user_dict.pop('password')
    new_user = User(**user_dict)
    new_user.password = get_password_hash(password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}