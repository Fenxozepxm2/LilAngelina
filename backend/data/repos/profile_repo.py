from sqlalchemy.orm import Session, selectinload
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

    def check_user_reg(self, db: Session, username) -> bool:
        return db.query(User).filter_by(username=username).first() is not None

    def find_user_by_username(self, db: Session, username):
        try:
            return db.query(User).filter_by(username=username).first()
        except ValueError as e:
            raise e
        
    def get_user_orders(self, db: Session, user_id: int) -> dict:
        return db.query(Order).options(selectinload(Order.items)).filter(Order.user_id == user_id).all()
    
    def add_user_order(self, db: Session, user_data: dict, user_id: int, cart_items: dict) -> dict:
        # Создаём заказ
        order = Order(
            status="в обработке",
            first_name_usr=user_data.get("first_name"),
            last_name_usr=user_data.get("last_name"),
            surname=user_data.get("surname"),
            adress=user_data.get("adress"),
            user_id=user_id,
            amount=0  # временно, потом обновим
        )
        db.add(order)
        db.flush()  # чтобы получить order.id

        total = 0
        for item in cart_items:
            order_item = OrderItem(
                item_type=item["item_type"],
                quantity=item["quantity"],
                item_id=item["item_id"],
                price=item["price"],
                order_id=order.id
            )
            db.add(order_item)
            total += item["price"] * item["quantity"]
        
        order.amount = total + (order.commission or 0)  # комиссия по умолчанию 5
        db.commit()
        db.refresh(order)  # подгружаем связанные items (если связь настроена на lazy='select')

        return {
            "id": order.id,
            "commission": order.commission,
            "amount": order.amount,
            "status": order.status,
            "first_name_usr": order.first_name_usr,
            "last_name_usr": order.last_name_usr,
            "surname": order.surname,
            "adress": order.adress,
            "items": [
                {
                    "id": i.id,
                    "item_type": i.item_type,
                    "quantity": i.quantity,
                    "item_id": i.item_id,
                    "price": i.price
                }
                for i in order.items
            ]
        }
        
        