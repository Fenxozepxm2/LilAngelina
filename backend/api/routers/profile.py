import asyncio
from datetime import datetime, timedelta, timezone
import json
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from domain.models import UserAuthSchema
import httpx  
from dependencies import get_session, get_db
from data.services.profile_service import LilAngelinaService
from sqlalchemy.orm import Session
from main import settings
import jwt


profile_router = APIRouter(tags=["profile"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')


def generate_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)




@profile_router.post("/auth/register")
def register_user(user_data: UserAuthSchema):

    hashed_password = pwd_context.hash(user_data.password)

    






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