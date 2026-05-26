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
from main import settings
from passlib.context import CryptContext
from data.models.models_db import User
import jwt


service = LilAngelinaService()

orders_page_router = APIRouter(tags=['orders', 'client'])


@orders_page_router.get('/orders')
def orders_page(db: Session, user: User = Depends(service.get_current_user)):
    orders = service.lil_repo.get_user_orders(db, user.id)
    return [{
        "id": o.id,
        "commission": o.commission,
        "amount": o.amount,
        "status": o.status,
        "first_name_usr": o.first_name_usr,
        "last_name_usr": o.last_name_usr,
        "surname": o.surname | None,
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
def add_order(db: Session, cart: dict, user: User = Depends(service.get_current_user)):
    service.lil_repo.add_user_order(db, user,user.id, cart)
    return {
        
    }

