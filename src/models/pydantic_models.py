import re
from pydantic import BaseModel, EmailStr, validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    age: int

    @validator('username')
    def username_validator(cls, v):
        if len(v) < 3:
            raise ValueError('Имя пользователя должно содержать минимум 3 символа')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Имя пользователя может содержать только буквы, цифры и нижнее подчеркивание')
        return v

    @validator('age')
    def age_validator(cls, v):
        if v <= 0 or v >= 100:
            raise ValueError('Возраст должен быть больше 0 и меньше 100')
        return v


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int

    @validator('quantity')
    def quantity_validator(cls, v):
        if v <= 0:
            raise ValueError('Количество должно быть больше 0')
        return v


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int

    class Config:
        from_attributes = True  # Заменили orm_mode на from_attributes