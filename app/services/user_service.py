from sqlalchemy.orm import Session
from app.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, username: str):
        return self.db.query(User).filter(User.email == username).first()

