from sqlalchemy.orm import Session
from sqlalchemy import inspect
from data.models.models_db import Poster, Disko, Order, OrderItem, User
from datetime import datetime




class LilangelinaRepo():
    def get_posters(self, db: Session):
        return db.query(Poster).all()

    def get_disks(self, db: Session):
        return db.query(Disko).all()

    def get_disk(self, db: Session, id: int):
        return db.query(Disko).filter_by(id=id).first()

    def get_poster(self, db: Session, id: int):
        return db.query(Poster).filter_by(id=id).first()
    
    def add_user(self, db: Session, username: str, hashed_password: str, phone: str, mail: str):
        user = User(
            username=username,
            hashed_password=hashed_password,
            phone=phone,
            mail=mail
        )
        db.add(user)
        db.commit()

    def check_user(self, db: Session, username):
        return db.query(User).filter_by(username=username).first()


    