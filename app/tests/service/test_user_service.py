import pytest
import uuid
from sqlalchemy.exc import NoResultFound
from pydantic import ValidationError
from fastapi_pagination import Params, Page

from app.schemas.user import UserCreate, UserUpdate, UserPartialUpdate
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
        # Given
        params = Params(page=1, size=10)

        # When
        users_page = service_user.get_users(db, params)

        # Then
        assert isinstance(users_page, Page)
        assert users_page.total == 0
        assert len(users_page.items) == 0

    def test_list_users_with_data(self, db, multiple_users):
        # Given
        params = Params(page=1, size=10)

        # When
        users_page = service_user.get_users(db, params)

        # Then
        assert isinstance(users_page, Page)
        assert users_page.total == 5
        assert len(users_page.items) == 5


class TestUserRetrieveService:
    def test_get_user_by_id_success(self, db, user):
        # Given and when
        fetched = service_user.get_user_by_id(db, user.id)

        # Then
        assert fetched.id == user.id
        assert fetched.username == "username"

    def test_get_user_by_id_not_found(self, db):
        # Given when and then
        with pytest.raises(NoResultFound):
            service_user.get_user_by_id(db, uuid.uuid4())


class TestUserUpdateService:
    def test_update_user_put(self, db, user):
        # Given
        update_data = UserUpdate(
            username="after",
            email="after@example.com",
            first_name="New",
            last_name="Name",
            role="admin",
        )

        # When
        updated = service_user.update_user(db, user.id, update_data)

        # Then
        assert updated.username == "after"
        assert updated.email == "after@example.com"
        assert updated.role == "admin"

    def test_update_user_patch(self, db, user):
        # Given
        update_data = UserPartialUpdate(first_name="Updated")

        # When
        updated = service_user.update_user(db, user.id, update_data)

        # Then
        assert updated.username == "username"
        assert updated.first_name == "Updated"

    def test_update_user_not_found(self, db):
        # Given and when
        update_data = UserPartialUpdate(first_name="NewName")

        # Then
        with pytest.raises(NoResultFound):
            service_user.update_user(db, uuid.uuid4(), update_data)

    def test_update_user_missing_fields(self, db):
        # Given when and then
        with pytest.raises(ValidationError):
            UserUpdate(first_name="NewName")


class TestUserDeleteService:
    def test_delete_user_success(self, db, user):
        # Given and when
        service_user.delete_user(db, user.id)

        # THen
        with pytest.raises(NoResultFound):
            service_user.get_user_by_id(db, user.id)

    def test_delete_user_not_found(self, db):
        # Given when and then
        with pytest.raises(NoResultFound):
            service_user.delete_user(db, uuid.uuid4())
