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
from passlib.context import CryptContext
import jwt



profile_router = APIRouter(tags=["profile"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(cin_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(cin_password, hashed_password)


def generate_jwt_token(username) -> dict:
    # Access Token на 15 минут
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    access_token = jwt.encode({"sub": username, "exp": access_expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Refresh Token на 7 дней
    refresh_expire = datetime.now(timezone.utc) + timedelta(days=7)
    refresh_token = jwt.encode({"sub": username, "exp": refresh_expire}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
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
    

@profile_router.post("/auth/login")
def login_user(responce: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
 
    user = service.lil_repo.find_user_by_username(db,form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="пользователь не найден", headers={"WWW-Authenticate": "Bearer"})

    access_token = generate_jwt_token(form_data.username)

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
        "user_id": user.username
    }

@profile_router.post("/token/refresh")
def refresh_access_token(responce: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="refresh token отсутсвует")
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        username: str= payload.get("sub")
    except jwt.PyJWKError:
        raise HTTPException(status_code=401, detail="refresh token истёк")

    new_tokens = generate_jwt_token(username)

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
        "user_id": username
    }

# @profile_router.get("/profile/user/{username}", tags=["Profile"])
# async def get_profile_user(username: str,
#                             client: httpx.AsyncClient = Depends(get_session),
#                               db: Session = Depends(get_db)):
#     service = LiChhessService(db,client)
#     statz = await service.show_statz(username)
#     return statz
    


# @profile_router.get("/profile/user/{username}/RatingHistory", tags=["Profile"])
# async def get_ratinghistory_user(username: str, session: httpx.AsyncClient = Depends(get_session)):
#     lichess_api_url = f"https://lichess.org/api/user/{username}/rating-history"
#     try:
#             responce = await session.get(lichess_api_url)
#             responce.raise_for_status()
#             data = responce.json()
#             rating_history_list = [RatingHistory(**item) for item in data]
#             return rating_history_list
#     except httpx.HTTPStatusError as e:
#         raise e
    
# @profile_router.get("/game/{gameId}", tags=["Games"])
# async def get_game_stat(gameId: str, session: httpx.AsyncClient = Depends(get_session)):
#     lichess_api_url = f"https://lichess.org/game/export/{gameId}"
#     headers = {"Accept": "application/json"}
#     try:
#             responce = await session.get(lichess_api_url, headers=headers)
#             responce.raise_for_status()
#             game = GameJson(**responce.json())
#             return game
#     except httpx.HTTPStatusError as e:
#         raise e

# # список матчей
# @profile_router.get("/profile/games/{username}")
# async def game_list(username: str, params: GamesRequestParams = Depends(), session: httpx.AsyncClient = Depends(get_session)):
#     # username = "BelyakovBogdan"
#     headers = {"Accept": "application/x-ndjson"}
#     # now = datetime.now()
#     # qwe = now - timedelta(days=20)
#     # params.until = int(qwe.timestamp()* 1000)
#     # # params.max = 100
#     lichess_api_url = f"https://lichess.org/api/games/user/{username}?max=20"
#     game_list = []
#     try:
#             responce = await session.get(lichess_api_url, headers=headers)
#             responce.raise_for_status()
#             await asyncio.sleep(0.05)
#             for item in responce.text.strip().split('\n'):
#                 if not item:
#                     continue
#                 gameData = json.loads(item)
#                 game = GameJson(**gameData)
#                 game_list.append(game)
#             return game_list
#     except httpx.HTTPStatusError as e:
#         raise e