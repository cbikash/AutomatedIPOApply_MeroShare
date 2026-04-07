from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey


class Sharelog(BaseModel):
    __tablename__ = 'sharelogs'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    meroshare_id = Column(Integer, ForeignKey('meroshares.id'), nullable=True)
    share_name = Column(String(200), default=None, nullable=True)
    share_code = Column(String(100), default=None, nullable=True)
    application_date = Column(String(100), default=None, nullable=True)
    status = Column(String(100), default=None, nullable=True)
    message = Column(String(500), default=None, nullable=True)
    response_data = Column(String(1000), default=None, nullable=True)
    applied_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    




