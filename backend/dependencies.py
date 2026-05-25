from data.models.database import SessionLocal
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI, Request
import httpx





def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_session(request: Request) -> httpx.AsyncClient:
    # Эта зависимость будет получать клиента из состояния приложения
    return request.app.state.session