from fastapi import FastAPI
from app.routers import meroshare
from sqlalchemy import engine
from app.core.database import Base
from cryptography.fernet import Fernet

def create_table():
    Base.metadata.create_all(bind=engine)

def startup_application():
    app = FastAPI()
    return app 

app = startup_application()
app.include_router(router=meroshare.router, prefix='/api/v1')