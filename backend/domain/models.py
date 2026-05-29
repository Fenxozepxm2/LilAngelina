from pydantic import BaseModel, Field, model_validator, field_validator, EmailStr
from typing import Optional, Union, Any, Literal, List
import datetime
from datetime import date, datetime


# ---------------------------------------------- МОДЕЛИ ПРОФИЛЯ ----------------------------------------------






class UserAuthSchema(BaseModel):
    # Разрешены только английские буквы (регистр не важен), цифры и "_"
    # Длина от 3 до 20 символов
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    
    # В пароле разрешаем любые символы, так как bcrypt защитит от SQLi
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=64,
    )

    mail: EmailStr | None = Field()

    phone: str | None = Field(
        pattern=r"^(?:\+7|7|8)\d{10}$",
    )


class CartItemSchema(BaseModel):
    item_type: str   # "poster" или "disk"
    item_id: int
    quantity: int
    price: int

class OrderRequest(BaseModel):
    first_name: str
    last_name: str
    surname: Optional[str] = None
    address: str
    items: List[CartItemSchema]






