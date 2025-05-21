class TestUserCreateAPI:
    def test_create_user_endpoint(self, client):
        # Given
        data = {
            "username": "john3",
            "email": "john3@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "admin",
        }

        # When
        response = client.post("/users/", json=data)

        # Then
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "john3"
        assert data["email"] == "john3@example.com"

    def test_create_user_missing_fields(self, client):
        # Given
        data = {
            "username": "john4",
            "first_name": "John",
            "last_name": "Doe",
            "role": "admin",
        }

        # When
        response = client.post("/users/", json=data)

        # THen
        assert response.status_code == 421

    def test_create_user_invalid_email(self, client):
        # Given
        data = {
            "username": "john5",
            "email": "not-an-email",
            "first_name": "John",
            "last_name": "Doe",
            "role": "admin",
        }

        # When
        response = client.post("/users/", json=data)

        # Then
        assert response.status_code == 422

    def test_create_user_invalid_role(self, client):
        # Given
        data = {
            "username": "john6",
            "email": "john6@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "invalid_role",
        }

        # When
        response = client.post("/users/", json=data)

        # Then
        assert response.status_code == 422

    def test_create_user_duplicate_username(self, client):
        # Given
        data = {
            "username": "dupuser",
            "email": "first@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "user",
        }
        client.post("/users/", json=data)
        data["email"] = "other@example.com"

        # When
        response = client.post("/users/", json=data)

        # Then
        assert response.status_code == 400

    def test_create_user_duplicate_email(self, client):
        # Given
        data = {
            "username": "user1",
            "email": "dupemail@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "role": "guest",
        }
        client.post("/users/", json=data)
        data["username"] = "user2"

        # When
        response = client.post("/users/", json=data)

        # Then
        assert response.status_code == 400


class TestUserListAPI:
    def test_list_users_endpoint(self, client):
        # Given and when
        response = client.get("/users/")

        # Then
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_users_endpoint_with_data(self, client, multiple_users):
        # Given and when
        response = client.get("/users/")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
