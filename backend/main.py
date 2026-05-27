from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
from api import main_router 
from contextlib import asynccontextmanager


from pydantic_settings import BaseSettings, SettingsConfigDict
from data.models.models_db import Base
from data.models.database import engine


class Set_Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config =  SettingsConfigDict(env_file=".env")


settings = Set_Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Base.metadata.create_all(bind=engine)
    client = httpx.AsyncClient()
    app.state.session = client
    yield
    await client.aclose()

app = FastAPI(title="LilAngelina", description="постеры и диски", lifespan=lifespan)

app.include_router(main_router)


origins = [
    "http://localhost:5173", # Адрес React-приложения
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
    