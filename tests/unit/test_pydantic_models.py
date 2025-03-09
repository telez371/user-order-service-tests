import pytest
from pydantic import ValidationError

from src.models.pydantic_models import UserCreate, UserResponse, OrderCreate, OrderResponse

class TestUserCreateModel:
    def test_valid_user_create(self):
        user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "age": 25
        }
        user = UserCreate(**user_data)
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.age == 25

    def test_invalid_username_short(self):
        user_data = {
            "username": "jo",
            "email": "john@example.com",
            "age": 25
        }
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        assert "Имя пользователя должно содержать минимум 3 символа" in str(exc_info.value)

    def test_invalid_username_format(self):
        user_data = {
            "username": "john@doe",
            "email": "john@example.com",
            "age": 25
        }
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        assert "Имя пользователя может содержать только буквы, цифры и нижнее подчеркивание" in str(exc_info.value)

    def test_invalid_email(self):
        user_data = {
            "username": "john_doe",
            "email": "invalid-email",
            "age": 25
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_invalid_age_negative(self):
        user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "age": -5
        }
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        assert "Возраст должен быть больше 0 и меньше 100" in str(exc_info.value)

    def test_invalid_age_too_large(self):
        user_data = {
            "username": "john_doe",
            "email": "john@example.com",
            "age": 150
        }
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)
        assert "Возраст должен быть больше 0 и меньше 100" in str(exc_info.value)


class TestOrderCreateModel:
    def test_valid_order_create(self):
        order_data = {
            "user_id": 1,
            "product_name": "Laptop",
            "quantity": 2
        }
        order = OrderCreate(**order_data)
        assert order.user_id == 1
        assert order.product_name == "Laptop"
        assert order.quantity == 2

    def test_invalid_quantity_zero(self):
        order_data = {
            "user_id": 1,
            "product_name": "Laptop",
            "quantity": 0
        }
        with pytest.raises(ValidationError) as exc_info:
            OrderCreate(**order_data)
        assert "Количество должно быть больше 0" in str(exc_info.value)

    def test_invalid_quantity_negative(self):
        order_data = {
            "user_id": 1,
            "product_name": "Laptop",
            "quantity": -1
        }
        with pytest.raises(ValidationError) as exc_info:
            OrderCreate(**order_data)
        assert "Количество должно быть больше 0" in str(exc_info.value)