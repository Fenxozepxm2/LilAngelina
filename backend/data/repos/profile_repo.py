from sqlalchemy.orm import Session
from sqlalchemy import inspect
from data.models.models_db import Poster, Disko, Order, OrderItem, User
from datetime import datetime



class LilangelinaRepo():
    def get_posters(self, db: Session):
        return db.query(Poster).all()









    