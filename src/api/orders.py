from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.models.pydantic_models import OrderCreate, OrderResponse
from src.models.orm_models import User, Order
from src.database.db import get_db

# Создаем роутер для заказов
router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Заказ не найден"}}
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый заказ",
    description="Создание нового заказа для указанного пользователя"
)
def create_order(
        order: OrderCreate,
        db: Session = Depends(get_db)
):
    """
    Создаёт новый заказ с предоставленными данными:

    - **user_id**: ID пользователя, для которого создаётся заказ
    - **product_name**: наименование продукта
    - **quantity**: количество (больше 0)

    Возвращает созданный заказ с присвоенным id.
    """
    # Проверяем существование пользователя
    user = db.query(User).filter(User.id == order.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    db_order = Order(
        user_id=order.user_id,
        product_name=order.product_name,
        quantity=order.quantity
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Получить данные заказа",
    description="Получение данных заказа по указанному ID"
)
def get_order(
        order_id: int,
        db: Session = Depends(get_db)
):
    """
    Получает данные заказа по указанному ID:

    - **order_id**: ID заказа (целое число)

    Возвращает данные заказа или 404, если заказ не найден.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден"
        )
    return db_order


@router.get(
    "",
    response_model=List[OrderResponse],
    summary="Получить список всех заказов",
    description="Получение списка всех заказов в системе"
)
def get_all_orders(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Получает список всех заказов с возможностью пагинации:

    - **skip**: количество пропускаемых записей (для пагинации)
    - **limit**: максимальное количество возвращаемых записей

    Возвращает список заказов.
    """
    return db.query(Order).offset(skip).limit(limit).all()