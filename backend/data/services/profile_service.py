### будет обновлять профиль нашего игрока в БД

# <!-- проверить данные на устаревание  -->
# обновить БД и вернуть фронту
from sqlalchemy.orm import Session
import httpx
from httpx import AsyncClient  
from data.repos.profile_repo import LilangelinaRepo 
from data.adapters.profile_adapter import LiChessAdapter
from domain.models import PlayerStats
from domain.functions import calculate_stat_all_matches




class LilAngelinaService():
    def __init__(self, db: Session):
        self.db = db
        self.lil_repo = LilangelinaRepo()

    def show_posters(self):
        return self.lil_repo.get_posters(self.db)

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
