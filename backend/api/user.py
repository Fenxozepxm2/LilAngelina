from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from config import settings
from dependencies import get_db
from data.models.models_db import User
from data.repos.profile_repo import LilangelinaRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')   # обрати внимание на путь

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось валидировать токен",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    repo = LilangelinaRepo()
    user = repo.find_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user