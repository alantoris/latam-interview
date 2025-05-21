from pydantic import ValidationError
import pytest
from fastapi import HTTPException
from app.schemas.user import UserCreate
from app.services import user as service_user
from app.services.exceptions import DuplicateUserError


class TestUserCreateService:
    def test_create_user(self, db):
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

    def test_create_user_duplicate_username(self, db):
        # Given
        user_data1 = UserCreate(
            username="duplicate",
            email="unique1@example.com",
            first_name="A",
            last_name="B",
            role="admin",
        )
        service_user.create_user(db, user_data1)

        # When
        user_data2 = UserCreate(
            username="duplicate",
            email="unique2@example.com",
            first_name="C",
            last_name="D",
            role="user",
        )

        # Then
        with pytest.raises(DuplicateUserError) as exc_info:
            service_user.create_user(db, user_data2)

    def test_create_user_duplicate_email(self, db):
        # Given
        user_data1 = UserCreate(
            username="unique_username1",
            email="duplicate@example.com",
            first_name="A",
            last_name="B",
            role="user",
        )
        service_user.create_user(db, user_data1)

        # When
        user_data2 = UserCreate(
            username="unique_username2",
            email="duplicate@example.com",
            first_name="C",
            last_name="D",
            role="guest",
        )

        # Then
        with pytest.raises(DuplicateUserError) as exc_info:
            service_user.create_user(db, user_data2)

    def test_create_user_invalid_role(self, db):
        # Given when and then
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                first_name="Test",
                last_name="User",
                role="invalid_role",
            )


class TestUserListService:
    def test_list_users_empty(self, db):
        # Given and When
        users = service_user.get_users(db)

        # Then
        assert len(users) == 0

    def test_list_users_with_data(self, db, multiple_users):
        # Given and When
        users = service_user.get_users(db)

        # Then
        assert len(users) == 5
