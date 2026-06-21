from pydantic import BaseModel, Field, model_validator, field_validator, EmailStr
from typing import Optional, Union, Any, Literal, List
import datetime
from datetime import date, datetime
import re
from pydantic import BaseModel, Field, EmailStr, field_validator


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
    adress: str
    items: List[CartItemSchema]


PHONE_REGEX = re.compile(r"^\+\d{1,3}\d{1,14}$")


class UserContacts(BaseModel):
    # Теперь все поля могут принимать None и по умолчанию равны None
    mail: Optional[EmailStr] = Field(default=None)
    
    phone: Optional[str] = Field(default=None, description="Телефон в формате +79991234567")
    
    # min_length убран из Field, так как None имеет длину 0 и вызвал бы ошибку
    adres: Optional[str] = Field(default=None, max_length=255)

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, value: Optional[str]) -> Optional[str]:
        # Если поле не заполнено, сразу возвращаем None без валидации
        if value is None:
            return None
            
        normalized = value.replace(" ", "").replace("-", "")
        if not PHONE_REGEX.match(normalized):
            raise ValueError(
                "Некорректный формат телефона. Используйте международный формат (например, +79991234567)"
            )
        return normalized

    @field_validator("adres")
    @classmethod
    def validate_address_content(cls, value: Optional[str]) -> Optional[str]:
        # Если поле не заполнено, пропускаем валидацию
        if value is None:
            return None
            
        stripped = value.strip()
        if len(stripped) < 10:
            raise ValueError("Адрес слишком короткий или состоит только из пробелов")
        return stripped



class AddPoster(BaseModel):
    id: int
    name: str
    author: str
    price: int
    size: str
    poster_url: str
    edition: str
    

