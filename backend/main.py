from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
from api import main_router 
from contextlib import asynccontextmanager
from fastapi.openapi.utils import get_openapi


from data.models.models_db import Base
from data.models.database import engine




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



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Lil Angelina API",
        version="1.0.0",
        routes=app.routes,
    )
    # Принудительно устанавливаем схему безопасности
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi



if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
    