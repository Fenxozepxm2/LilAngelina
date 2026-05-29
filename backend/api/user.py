from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import settings


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')



def get_current_user(self, token: str= Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=401, detail="Не удалось валидировать токен", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str= payload.get("sub")
        if not username:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = self.lil_repo.find_user_by_username(self.db, username)
    if not user:
        raise credentials_exception
    return user
