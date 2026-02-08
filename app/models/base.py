from sqlalchemy import Column,Integer,DateTime,Boolean
from sqlalchemy.sql import func
from app.core.database import Base
class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    is_deleted = Column(
        Boolean,
        nullable=False,
        default=False
    )
