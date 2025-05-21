from app.schemas.user import UserCreate
from app.services import user as service_user


def test_create_user(db):
    # Given
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        role="admin",
    )

    # When
    user = service_user.create_user(db, user_data)

    # Then
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "admin"


def test_list_users_with_data(db, multiple_users):
    # Given and When
    users = service_user.get_users(db)

    # Then
    assert len(users) == 5
