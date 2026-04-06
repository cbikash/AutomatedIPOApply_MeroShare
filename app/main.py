from fastapi import FastAPI
from app.routers import meroshare, google_auth, user
from sqlalchemy import engine
from app.core.database import Base
from cryptography.fernet import Fernet
from starlette.middleware.sessions import SessionMiddleware
from app.core.setting import Settings



def create_table():
    Base.metadata.create_all(bind=engine)

def startup_application():
    app = FastAPI()
    return app 

app = startup_application()
app.add_middleware(
    SessionMiddleware,
    secret_key=Settings.SECRET_KEY,  # use env variable in production
)
app.include_router(router=meroshare.router, prefix='/api/v1')
app.include_router(router=google_auth.router, prefix='/api/v1')
app.include_router(router=user.router, prefix='/api/v1')