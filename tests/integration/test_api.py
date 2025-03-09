class TestUserAPI:
    def test_create_user(self, client, db_session):
        user_data = {
            "username": "johndoe",
            "email": "john@example.com",
            "age": 30
        }
        response = client.post("/users", json=user_data)

        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert data["username"] == "johndoe"
        assert data["email"] == "john@example.com"
        assert data["age"] == 30

        user_id = data["id"]
        db_response = client.get(f"/users/{user_id}")
        assert db_response.status_code == 200
        assert db_response.json() == data

    def test_create_user_invalid_data(self, client):
        invalid_user_data = {
            "username": "j",
            "email": "john@example.com",
            "age": 30
        }
        response = client.post("/users", json=invalid_user_data)

        assert response.status_code == 422

    def test_create_duplicate_user(self, client, test_user):
        duplicate_user_data = {
            "username": test_user.username,
            "email": "different@example.com",
            "age": 30
        }
        response = client.post("/users", json=duplicate_user_data)

        assert response.status_code == 400
        assert "уже существует" in response.json()["detail"]

    def test_get_user(self, client, test_user):
        response = client.get(f"/users/{test_user.id}")

        assert response.status_code == 200

        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email
        assert data["age"] == test_user.age

    def test_get_nonexistent_user(self, client):
        non_existent_id = 9999
        response = client.get(f"/users/{non_existent_id}")

        assert response.status_code == 404  # Not Found
        assert "не найден" in response.json()["detail"]


class TestOrderAPI:
    def test_create_order(self, client, test_user):
        order_data = {
            "user_id": test_user.id,
            "product_name": "Test Product",
            "quantity": 2
        }
        response = client.post("/orders", json=order_data)

        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert data["user_id"] == test_user.id
        assert data["product_name"] == "Test Product"
        assert data["quantity"] == 2

        order_id = data["id"]
        db_response = client.get(f"/orders/{order_id}")
        assert db_response.status_code == 200
        assert db_response.json() == data

    def test_create_order_invalid_data(self, client, test_user):
        invalid_order_data = {
            "user_id": test_user.id,
            "product_name": "Test Product",
            "quantity": 0
        }
        response = client.post("/orders", json=invalid_order_data)
