from fastapi import APIRouter, Request, Depends
from app.schemas.user import UserCreate
from app.models.user import User
from sqlalchemy.orm import Session
from app.deps import get_db
from app.internal.jwt_utils import get_current_user, get_password_hash
from app.internal.encrypt import generate_encryption_key
from app.services.meroshare_service import MeroshareService

router = APIRouter(prefix='/users')

@router.get("/", tags=["users"])
def read_users(request: Request = None):
    ip = request.client.host
    return {"message": f"Hello, your IP address is {ip}"}

@router.post("/", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_dict = user.model_dump()
    password = user_dict.pop('password')
    new_user = User(**user_dict)
    new_user.password = get_password_hash(password)
    new_user.key = generate_encryption_key()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/generate-key" , tags=["users"])
def generate_key(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    key = generate_encryption_key()
    
    try:
        meroshareService = MeroshareService(db, key=key)
        meroshareServicedecrypted = MeroshareService(db, key=current_user.key)

        meroshare_accounts = current_user.meroshare_accounts

        for account in meroshare_accounts:
            try:
                account.username = meroshareService.encrypt_username(meroshareServicedecrypted.decrypt_username(account.username))
                account.password = meroshareService.encrypt_password(meroshareServicedecrypted.decrypt_password(account.password))
                account.crn = meroshareService.encrypt_crn(meroshareServicedecrypted.decrypt_crn(account.crn))
                account.pin = meroshareService.encrypt_pin(meroshareServicedecrypted.decrypt_pin(account.pin))
                db.add(account)
            except Exception as e:
                raise e

        current_user.key = key
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    except Exception as e:
        db.rollback()
        raise e

    return {"message": "Encryption key generated and applied to all Meroshare accounts successfully"}