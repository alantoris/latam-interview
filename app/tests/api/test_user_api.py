def test_create_user_endpoint(client):
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


def test_list_users_endpoint(client):
    # Given and when
    response = client.get("/users/")

    # Then
    print(response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_users_endpoint_with_data(client, multiple_users):
    # Given and when
    response = client.get("/users/")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
