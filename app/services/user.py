from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import List
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.exceptions import DuplicateUserError


def get_user_by_id(db: Session, user_id: UUID) -> User:
    """
    Retrieves a specific user in the database.

    Args:
        db (Session): Database session.
        user_id (UUID): UUID from te user to get from the database.

    Raises:
        NoResultFound: If user is not found.

    Returns:
        User: User object.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NoResultFound("User not found")
    return user


def get_users(db: Session) -> List[User]:
    """
    Retrieves all existing users in the database.

    Args:
        db (Session): Database session.

    Returns:
        List[User]: List of User objects.
    """
    return db.query(User).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Creates a new user in the database.

    Args:
        db (Session): Database session.
        user_in (UserCreate): New user data.

    Raises:
        DuplicateUserError: If the username or email address is already registered.

    Returns:
        User: Newly created User object.
    """
    user = User(**user_in.model_dump())
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise DuplicateUserError("Username or email already exists")


def update_user(db: Session, user_id: UUID, user_in: UserUpdate) -> User:
    """
    Update a user in the database.

    Args:
        db (Session): Database session.
        user_id (UUID): UUID from te user to update from the database.
        user_in (UserCreate): New user data.

    Raises:
        NoResultFound: If user is not found.
        DuplicateUserError: If the username or email address is already registered.

    Returns:
        User: Updated User object.
    """
    user = get_user_by_id(db, user_id)
    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise DuplicateUserError("Username or email already exists")


def delete_user(db: Session, user_id: UUID) -> None:
    """
    Update a user in the database.

    Args:
        db (Session): Database session.
        user_id (UUID): UUID from te user to delete from the database.

    Raises:
        NoResultFound: If user is not found.
    """
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
