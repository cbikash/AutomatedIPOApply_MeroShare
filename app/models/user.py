from sqlalchemy import Column,Integer,String,Boolean, Index
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'
    
    name = Column(String(200), default= None, nullable=True)
    email = Column(String(200), default=None, nullable=True, unique=True, index=True)
    password = Column(String(200), default=None, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)