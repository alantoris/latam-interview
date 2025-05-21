from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate


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
        HTTPException: If the username or email address is already registered.

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )
