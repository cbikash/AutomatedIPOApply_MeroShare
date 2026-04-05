from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth 
from app.core.setting import Settings
from app.internal.jwt_utils import create_access_token, verify_password, get_password_hash
from datetime import timedelta
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models.user import User
from app.internal.response import success_response, error_response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from app.services.user_service import UserService

router = APIRouter(prefix='/auth')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

oauth = OAuth()
oauth.register(
    name="google",
    client_id=Settings.GOOGLE_CLIENT_ID,
    client_secret=Settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope" : "openid email profile"
    }
)


def authenticate_user(db: Session, username: str, password: str):
    user = UserService(db).get_user(username=username)
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, username=form_data.username, password=form_data.password)

    if not user:
        return error_response(message='Invalid username or password.')
    
    access_token = create_access_token(
        data={'sub': user.email, 'name' : user.name, 'provider' : 'local'},
        expires_delta=timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_HOURS),
    )

    return  success_response(data={
        'token': access_token,
        'token_type': 'bearer',
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    })


@router.get("/test")
async def test_endpoint(db: Session = Depends(get_db)):

    has_p = get_password_hash("password123")

    return {"message": "This is a protected endpoint", "token": has_p}


@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):

    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo") or {}

        username = user_info.get('email')

        user = db.query(User).filter(
            (User.email == username)
        ).first()

        if not user:
            return error_response(message='User not found.')

        access_token = create_access_token(
            data={'sub': username, 'name' : user.name, 'provider' : 'google'},
            expires_delta=timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_HOURS),
        )

        return  success_response(data={
            'token': access_token,
            'token_type': 'bearer',
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        })
    
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())
        return {"error": str(e)}

