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
from data.models.models_db import User
import jwt
from api.user import get_current_user
from domain.models import OrderRequest, CartItemSchema
from fastapi.encoders import jsonable_encoder



orders_page_router = APIRouter(tags=['orders'])


@orders_page_router.get('/orders')
def orders_page(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    service = LilAngelinaService(db)
    orders = service.lil_repo.get_user_orders(db, user.id)
    return [{
        "id": o.id,
        "commission": o.commission,
        "amount": o.amount,
        "status": o.status,
        "first_name_usr": o.first_name_usr,
        "last_name_usr": o.last_name_usr,
        "surname": o.surname if o.surname else None,
        "items":[ {
            "id": i.id,
            "order_id": i.order_id,
            "item_type": i.item_type,
            "quantity": i.quantity,
            "item_id": i.item_id,
            "price": i.price
        }
        for i in o.items
        ],
        "adress": o.adress
        }
    for o in orders
    ] 

@orders_page_router.post("/add_order")
def add_order(order_req: OrderRequest, user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    user_data = {
        "first_name": order_req.first_name,
        "last_name": order_req.last_name,
        "surname": order_req.surname,
        "adress": order_req.adress,
    }
    cart_items = [item.dict() for item in order_req.items]
    order = service.lil_repo.add_user_order(db, user_data, user.id, cart_items)
    return order


@orders_page_router.get("/order/{order_id}")
def get_order_info(order_id, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    order = service.show_user_order_info(user.id, order_id)
    return jsonable_encoder(order,exclude="commision")
    