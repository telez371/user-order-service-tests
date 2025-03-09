import pytest
from sqlalchemy.exc import IntegrityError

from src.models.orm_models import User, Order


class TestUserCrudOperations:
    def test_create_user(self, db_session):
        user = User(
            username="johndoe",
            email="john@example.com",
            age=30
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None

        db_user = db_session.query(User).filter(User.id == user.id).first()
        assert db_user is not None
        assert db_user.username == "johndoe"
        assert db_user.email == "john@example.com"
        assert db_user.age == 30

    def test_create_duplicate_username(self, db_session, test_user):
        duplicate_user = User(
            username="testuser",
            email="different@example.com",
            age=25
        )
        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_create_duplicate_email(self, db_session, test_user):
        duplicate_user = User(
            username="different_user",
            email="test@example.com",
            age=25
        )
        db_session.add(duplicate_user)

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_get_user_by_id(self, db_session, test_user):
        db_user = db_session.query(User).filter(User.id == test_user.id).first()

        assert db_user is not None
        assert db_user.id == test_user.id
        assert db_user.username == test_user.username
        assert db_user.email == test_user.email
        assert db_user.age == test_user.age

    def test_get_nonexistent_user(self, db_session):
        non_existent_id = 9999
        db_user = db_session.query(User).filter(User.id == non_existent_id).first()

        assert db_user is None


class TestOrderCrudOperations:
    def test_create_order(self, db_session, test_user):
        order = Order(
            user_id=test_user.id,
            product_name="Test Product",
            quantity=3
        )
        db_session.add(order)
        db_session.commit()

        assert order.id is not None

        db_order = db_session.query(Order).filter(Order.id == order.id).first()
        assert db_order is not None
        assert db_order.user_id == test_user.id
        assert db_order.product_name == "Test Product"
        assert db_order.quantity == 3

    def test_create_order_nonexistent_user(self, db_session):
        non_existent_user_id = 9999
        order = Order(
            user_id=non_existent_user_id,
            product_name="Test Product",
            quantity=1
        )
        db_session.add(order)

        with pytest.raises(IntegrityError):
            db_session.commit()

        db_session.rollback()

    def test_get_order_by_id(self, db_session, test_order):
        db_order = db_session.query(Order).filter(Order.id == test_order.id).first()

        assert db_order is not None
        assert db_order.id == test_order.id
        assert db_order.user_id == test_order.user_id
        assert db_order.product_name == test_order.product_name
        assert db_order.quantity == test_order.quantity

    def test_get_nonexistent_order(self, db_session):
        non_existent_id = 9999
        db_order = db_session.query(Order).filter(Order.id == non_existent_id).first()

        assert db_order is None

    def test_order_relationship(self, db_session, test_order, test_user):
        db_order = db_session.query(Order).filter(Order.id == test_order.id).first()

        assert db_order.user is not None
        assert db_order.user.id == test_user.id
        assert db_order.user.username == test_user.username

        db_user = db_session.query(User).filter(User.id == test_user.id).first()
        assert len(db_user.orders) > 0
        assert db_user.orders[0].id == test_order.id
