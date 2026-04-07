from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

class Share(BaseModel):
    __tablename__ = 'shares'
    
    name = Column(String(200), default=None, nullable=True)
    code = Column(String(100), default=None, nullable=True)
    company_name = Column(String(200), default=None, nullable=True)
    company_code = Column(String(100), default=None, nullable=True)