from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import BaseModel
from app.models.user import User
from sqlalchemy.orm import relationship

class Meroshare(BaseModel):
    __tablename__ = 'meroshares'

    username = Column(String(200), default=None, nullable=True)
    password = Column(String(200), default=None, nullable=True)
    client_id = Column(String(200), default=None, nullable=True)
    crn = Column(String(200), default=None, nullable=True)
    pin = Column(String(200), default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # owner = relationship(
    #     'User',
    #     back_populates='meroshares'
    # )
