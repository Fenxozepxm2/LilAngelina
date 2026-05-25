from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Файл БД будет лежать в папке, откуда запущен uvicorn (скорее всего, backend/)
SQLALCHEMY_DATABASE_URL = "sqlite:///./lil_angelina_new.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()