### будет обновлять профиль нашего игрока в БД

# <!-- проверить данные на устаревание  -->
# обновить БД и вернуть фронту


from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import httpx
from httpx import AsyncClient  
from data.repos.profile_repo import LilangelinaRepo 
from domain.models import UserAuthSchema
from domain.functions import calculate_stat_all_matches
from passlib.context import CryptContext
from data.models.models_db import Poster, Disko, User



from config import settings
import jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

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
        if not self.lil_repo.check_user_reg(self.db, user_data.username):
            hashed_password = pwd_context.hash(user_data.password)
            self.lil_repo.add_user(self.db, 
                                   username=user_data.username,
                                   hashed_password=hashed_password,
                                   phone=user_data.phone,
                                   mail=user_data.mail
                                   )
        else:
            raise HTTPException(status_code=400, detail="user already register")
    

    def show_user_order_info(self, user_id, order_id):
        try:
            order = self.lil_repo.get_order_info(self.db, user_id, order_id)
            if not order:
                raise HTTPException(status_code=404, detail="Заказ не найден")
            
            items_data = []
            for item in order.items:
                # Получаем картинку в зависимости от типа
                if item.item_type == "poster":
                    poster = self.db.query(Poster).filter(Poster.id == item.item_id).first()
                    image_url = poster.poster_url if poster else ""
                else:  # disk
                    disk = self.db.query(Disko).filter(Disko.id == item.item_id).first()
                    image_url = disk.album_cover_url if disk else ""
                
                items_data.append({
                    "id": item.id,
                    "item_type": item.item_type,
                    "quantity": item.quantity,
                    "item_id": item.item_id,
                    "price": item.price,
                    "image_url": image_url
                })
            

        except HTTPException as e:
            raise HTTPException(status_code=404, detail="Заказ не найден")

        return {
                "id": order.id,
                "commission": order.commission,
                "amount": order.amount,
                "status": order.status,
                "first_name_usr": order.first_name_usr,
                "last_name_usr": order.last_name_usr,
                "surname": order.surname,
                "adress": order.adress,
                "items": items_data
            }
