import asyncio
from datetime import datetime, timedelta, timezone
import json
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from domain.models import UserAuthSchema
import httpx  
from dependencies import get_session, get_db
from data.services.profile_service import LilAngelinaService
from sqlalchemy.orm import Session
from config import settings
from data.models.models_db import User
from passlib.context import CryptContext
import jwt



profile_router = APIRouter(tags=["profile"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(cin_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(cin_password, hashed_password)


def generate_jwt_token(username, user_id) -> dict:
    # Access Token на 15 минут
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    access_token = jwt.encode({"sub": username, "user_id": user_id, "exp": access_expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Refresh Token на 7 дней
    refresh_expire = datetime.now(timezone.utc) + timedelta(days=7)
    refresh_token = jwt.encode({"sub": username, "user_id": user_id, "exp": refresh_expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return {"access_token": access_token, "refresh_token": refresh_token}




@profile_router.post("/auth/register")
def register_user_endp(user_data: UserAuthSchema, db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    check_usr = service.lil_repo.check_user_reg(db, user_data.username)
    if not check_usr:
        service.register_user(user_data)
        return {
            "200": "user succesed register"
        }
    else:
        raise HTTPException(status_code=400, detail="User already exists")
    

@profile_router.post("/auth/login")
def login_user(responce: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
 
    user = service.lil_repo.find_user_by_username(db,form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="пользователь не найден", headers={"WWW-Authenticate": "Bearer"})

    user_id = user.id
    access_token = generate_jwt_token(form_data.username, user_id)


    responce.set_cookie(
        key="refresh_token",
        value=access_token["refresh_token"],
        httponly=True, # защита от XSS
        secure=True, # только по HTTPS
        samesite="lax", # защита от CRSF
        max_age=7* 24 * 3600 # время жизни в секундах (7 дней)
    )    



    return {
        "access_token": access_token["access_token"],
        "token_type": "Bearer",
        "user_name": user.username,
        "user_id": user_id
    }

@profile_router.post("/token/refresh")
def refresh_access_token(responce: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="refresh token отсутсвует")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username: str= payload.get("sub")
        user_id: int=payload.get("user_id")
    except jwt.PyJWKError:
        raise HTTPException(status_code=401, detail="refresh token истёк")

    new_tokens = generate_jwt_token(username, user_id)

    responce.set_cookie(
        key="refresh_token",
        value=new_tokens["refresh_token"],
        httponly=True, # защита от XSS
        secure=True, # только по HTTPS
        samesite="lax", # защита от CRSF
        max_age=7* 24 * 3600 # время жизни в секундах (7 дней)
    ) 

    return {
        "access_token": new_tokens["access_token"],
        "token_type": "Bearer",
        "user_name": username,
        "user_id": user_id
    }
