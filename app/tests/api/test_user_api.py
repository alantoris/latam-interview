import uuid


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
        assert response.status_code == 422

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
        response = client.get("/users/?page=1&size=10")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["total"] == 0
        assert data["items"] == []
        assert data["page"] == 1
        assert data["size"] == 10

    def test_list_users_endpoint_with_data(self, client, multiple_users):
        # Given and when
        response = client.get("/users/?page=1&size=10")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["total"] == 5
        assert len(data["items"]) == 5
        assert data["page"] == 1
        assert data["size"] == 10


class TestUserRetrieveAPI:
    def test_retrieve_existing_user(self, client, user):
        # Given and When
        response = client.get(f"/users/{user.id}")

        # Then
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user.username
        assert data["email"] == user.email

    def test_retrieve_non_existing_user(self, client):
        # Given and When
        response = client.get(f"/users/{uuid.uuid4()}")

        # Then
        assert response.status_code == 404


class TestUserUpdateAPI:
    def test_update_user_success(self, client, user):
        # Given
        data = {
            "username": "updated_username",
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "role": "admin",
        }

        # When
        response = client.put(f"/users/{user.id}", json=data)

        # Then
        assert response.status_code == 200
        updated = response.json()
        assert updated["username"] == "updated_username"
        assert updated["email"] == "updated@example.com"

    def test_update_user_missing_fields(self, client, user):
        # Given
        data = {"first_name": "OnlyFirstName"}

        # When
        response = client.put(f"/users/{user.id}", json=data)

        # Then
        assert response.status_code == 422

    def test_update_user_invalid_email(self, client, user):
        # Given
        data = {
            "username": "u",
            "email": "invalid-email",
            "first_name": "Name",
            "last_name": "Last",
            "role": "user",
        }

        # When
        response = client.put(f"/users/{user.id}", json=data)

        # Then
        assert response.status_code == 422

    def test_update_user_not_found(self, client):
        # Given
        data = {
            "username": "updated_username",
            "email": "e@example.com",
            "first_name": "N",
            "last_name": "L",
            "role": "user",
        }

        # When
        response = client.put(f"/users/{uuid.uuid4()}", json=data)

        # Then
        assert response.status_code == 404


class TestUserPartialUpdateAPI:
    def test_partial_update_user_success(self, client, user):
        # Given
        data = {"first_name": "PatchedName"}

        # When
        response = client.patch(f"/users/{user.id}", json=data)

        # Then
        assert response.status_code == 200
        assert response.json()["first_name"] == "PatchedName"

    def test_partial_update_user_invalid_email(self, client, user):
        # Given
        data = {"email": "invalid"}

        # When
        response = client.patch(f"/users/{user.id}", json=data)

        # Then
        assert response.status_code == 422

    def test_partial_update_user_not_found(self, client):
        # Given and when
        response = client.patch(f"/users/{uuid.uuid4()}", json={"first_name": "X"})

        # Then
        assert response.status_code == 404


class TestUserDeleteAPI:
    def test_delete_user_success(self, client, user):
        # When
        response = client.delete(f"/users/{user.id}")

        # Then
        assert response.status_code == 204

        # Try to get user again
        get_response = client.get(f"/users/{user.id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client):
        # Given and when
        response = client.delete(f"/users/{uuid.uuid4()}")

        # Then
        assert response.status_code == 404
