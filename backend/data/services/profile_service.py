### будет обновлять профиль нашего игрока в БД

# <!-- проверить данные на устаревание  -->
# обновить БД и вернуть фронту


from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
import httpx
from httpx import AsyncClient  
from data.repos.profile_repo import LilangelinaRepo 
from domain.models import PlayerStats, UserAuthSchema
from domain.functions import calculate_stat_all_matches
from passlib.context import CryptContext
from api.routers.profile import oauth2_schema
from main import settings
import jwt



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(cin_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(cin_password, hashed_password)


class LilAngelinaService():
    def __init__(self, db: Session):
        self.db = db
        self.lil_repo = LilangelinaRepo()

    def show_posters(self):
        return self.lil_repo.get_posters(self.db)
    
    def show_disks(self):
        return self.lil_repo.get_disks(self.db)
    
    def show_disk(self, id):
        return self.lil_repo.get_disk(self.db, id)

    def show_poster(self, id):
        return self.lil_repo.get_poster(self.db, id)
    
    def register_user(self, user_data: UserAuthSchema):
        if not self.lil_repo.check_user_reg(user_data.username):
            hashed_password = pwd_context.hash(user_data.password)
            self.lil_repo.add_user(self.db, 
                                   username=user_data.username,
                                   hashed_password=hashed_password,
                                   phone=user_data.phone,
                                   mail=user_data.mail
                                   )
        else:
            raise HTTPException(status_code=400, detail="user already register")
        
    def get_current_user(self, token: str= Depends(oauth2_schema)):
        credentials_exception = HTTPException(status_code=401, detail="Не удалось валидировать токен", headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str= payload.get("sub")
            if not username:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        
        user = self.lil_repo.find_user_by_username(self.db, username)
        if not user:
            raise credentials_exception
        return user






# class LiChhessService():
#     def __init__(self, db: Session, client: httpx.AsyncClient):
#         self.db = db
#         self.client = client
#         self.profile_repo = LiChessRepos()
#         self.profile_adapter = LiChessAdapter(client)
        
        
#     async def show_statz(self, username: str):
#         # проверим есть ли такой пользователь в БД
#         user = self.profile_repo.get_user_profile(self.db, username)
#         # если нету создаём
#         if not user:
#             dataf_profile = await self.profile_adapter.fetch_profile(username)
#             dataf_rating = await self.profile_adapter.fetch_rating_history(username)
#             self.profile_repo.save_user_rofile(self.db, username,dataf_profile,dataf_rating)
#             games_json = await self.profile_adapter.fetch_games_history(username, max=200)
#             self.profile_repo.save_user_game(self.db, username, games_json)

#         # получаем данные из БД
#         profile_data_db = self.profile_repo.get_user_profile(self.db, username)
#         games_data_db = self.profile_repo.get_user_games(self.db, username)

#         # расчитываем статистику
#         statz = await calculate_stat_all_matches(profile_data_db)

#         return statz
