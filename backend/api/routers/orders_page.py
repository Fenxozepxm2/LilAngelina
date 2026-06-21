import asyncio
from datetime import datetime, timedelta, timezone
import json
from fastapi import FastAPI, HTTPException, APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic
from domain.models import UserAuthSchema
import httpx  
from dependencies import get_session, get_db
from data.services.profile_service import LilAngelinaService
from data.repos.profile_repo import LilangelinaRepo
from sqlalchemy.orm import Session
from config import settings
from passlib.context import CryptContext
from data.models.models_db import User, Poster, Disko, OrderAssignment
import jwt
from api.user import get_current_user
from domain.models import OrderRequest, CartItemSchema
from fastapi.encoders import jsonable_encoder



orders_page_router = APIRouter(tags=['orders'])


@orders_page_router.get('/api/orders')
def orders_page(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    service = LilAngelinaService(db)
    orders = service.lil_repo.get_user_orders(db, user.id)
    
    # Собираем ID товаров из всех заказов
    poster_ids = []
    disk_ids = []
    for order in orders:
        for item in order.items:
            if item.item_type == 'poster':
                poster_ids.append(item.item_id)
            else:
                disk_ids.append(item.item_id)
    
    # Словари {id: image_url}
    posters = {}
    if poster_ids:
        posters = {p.id: p.poster_url for p in db.query(Poster).filter(Poster.id.in_(poster_ids)).all()}
    disks = {}
    if disk_ids:
        disks = {d.id: d.album_cover_url for d in db.query(Disko).filter(Disko.id.in_(disk_ids)).all()}
    
    # Формируем ответ
    result = []
    for order in orders:
        items_data = []
        for item in order.items:
            image_url = None
            if item.item_type == 'poster':
                image_url = posters.get(item.item_id)
            else:
                image_url = disks.get(item.item_id)
            items_data.append({
                "id": item.id,
                "order_id": item.order_id,
                "item_type": item.item_type,
                "quantity": item.quantity,
                "item_id": item.item_id,
                "price": item.price,
                "image_url": image_url
            })
        result.append({
            "id": order.id,
            "commission": order.commission,
            "amount": order.amount,
            "status": order.status,
            "first_name_usr": order.first_name_usr,
            "last_name_usr": order.last_name_usr,
            "surname": order.surname if order.surname else None,
            "items": items_data,
            "adress": order.adress
        })
    return result

@orders_page_router.post("/api/add_order")
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


@orders_page_router.get("/api/order/{order_id}")
def get_order_info(order_id, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    order = service.show_user_order_info(user.id, order_id)
    return jsonable_encoder(order,exclude="commision")
    


@orders_page_router.get("/api/worker_{worker_id}/orders")
def get_workers_orders(worker_id: str, user: User = Depends(get_current_user) ,db: Session = Depends(get_db)):
    repo = LilangelinaRepo()
    worker_id = int(worker_id)
    if user.id == worker_id:

        orders = repo.get_worker_orders(db, worker_id)
        return orders
    else:
        return {
            "message" : "Отказано в доступе"
        }

@orders_page_router.patch("/api/worker_{worker_id}/orders/{order_id}}")
def patch_status_order(worker_id: str, order_id: str , data: dict, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    worker_id = int(worker_id)
    order_id = int(order_id)
    repo = LilangelinaRepo()
    if user.id == worker_id:
    
        try:
            status = data.get("status")
            if status:
                repo.patch_order(db, status, order_id)
        except ValueError as e:
            raise e
        
    else: 
        return {
            "message": "Отказано в доступе"
        }