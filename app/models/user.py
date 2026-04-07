from sqlalchemy import Column,Integer,String,Boolean, Index 
from app.models.base import BaseModel 
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = 'users'
    
    name = Column(String(200), default= None, nullable=True)
    email = Column(String(200), default=None, nullable=True, unique=True, index=True)
    password = Column(String(200), default=None, nullable=True)
    disabled = Column(Boolean, default=False, nullable=False)
    key = Column(String(256), default=None, nullable=True)

    # meroshare relationship
    meroshare_accounts = relationship(
        'Meroshare',
        back_populates='user',
        cascade='all, delete-orphan'
    )