from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

class Log(BaseModel):
    __tablename__ = 'logs'
    
    message = Column(String(500), default=None, nullable=True)
    level = Column(String(50), default=None, nullable=True)
    timestamp = Column(String(100), default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    