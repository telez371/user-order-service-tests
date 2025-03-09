from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from src.models.pydantic_models import UserCreate, UserResponse, OrderResponse
from src.models.orm_models import User, Order
from src.database.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Пользователь не найден"}}
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    description="Создание нового пользователя с указанными данными"
)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    db_user = User(
        username=user.username,
        email=user.email,
        age=user.age
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username или email уже существует"
        )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить данные пользователя",
    description="Получение данных пользователя по указанному ID"
)
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return db_user


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Получить список всех пользователей",
    description="Получение списка всех пользователей в системе"
)
def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):

    return db.query(User).offset(skip).limit(limit).all()


@router.get(
    "/{user_id}/orders",
    response_model=List[OrderResponse],
    summary="Получить заказы пользователя",
    description="Получение списка всех заказов указанного пользователя"
)
def get_user_orders(
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return db.query(Order).filter(Order.user_id == user_id).all()