from datetime import datetime

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List

class Base(DeclarativeBase):
    pass





class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=True)
    adres: Mapped[str] = mapped_column(nullable=True)

    orders: Mapped[List["Order"]] = relationship(back_populates="user")


class Poster(Base):
    __tablename__="posters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    size: Mapped[int] = mapped_column(nullable=True) # 1920px x 1080px
    edition: Mapped[str] = mapped_column() # из какого материала, в рамке/не в рамке
    poster_url: Mapped[str] = mapped_column()


class Disko(Base):
    __tablename__="disks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    album_name: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    edition: Mapped[str] = mapped_column() # типа золотой диск или серебрянный ты пон
    album_cover_url: Mapped[str] = mapped_column()
    about: Mapped[Optional[dict]] = mapped_column(JSON) # здесь будет более подробная инфа (год, список песен, информация о альбоме)


class OrderItem(Base):
    __tablename__="orderItems"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    item_type: Mapped[str] = mapped_column() # тип: Диск или Постер
    quantity: Mapped[int] = mapped_column() # кол-во
    item_id: Mapped[int] = mapped_column()
    price: Mapped[int] = mapped_column()

    order: Mapped[List["Order"]] = relationship(back_populates="items")


class Order(Base):
    __tablename__="orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    commission: Mapped[int] = mapped_column(server_default="5")
    amount: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column() # в процессе, в обработке, отправлен, готов, и т.д.
    first_name_usr: Mapped[str] = mapped_column()
    last_name_usr: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column(nullable=True)
    adress: Mapped[str] = mapped_column()

    # внешний ключ на таблицу User
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # связь с таблицей User
    user: Mapped[List["User"]] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(back_populates="order")



