import asyncio
from datetime import datetime, timedelta
import json
from fastapi import FastAPI, HTTPException, APIRouter, Depends
import httpx  
from dependencies import get_session, get_db
from data.services.profile_service import LilAngelinaService
from sqlalchemy.orm import Session




main_page_router = APIRouter(tags=['mainpage'])



@main_page_router.get("/posters")
def router_get_posters(db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    posters = service.show_posters()
    return posters


@main_page_router.get("/disks")
def router_get_disks(db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    disks = service.show_disks()
    return disks

@main_page_router.get("/disk/{id}")
def router_get_disk(id: int ,db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    disk = service.show_disk(id)
    return disk

@main_page_router.get("/poster/{id}")
def router_get_poster(id: int ,db: Session = Depends(get_db)):
    service = LilAngelinaService(db)
    poster = service.show_poster(id)
    return poster
