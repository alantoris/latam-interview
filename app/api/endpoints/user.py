from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas.user import UserOut, UserCreate
from app.services import user as service_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)) -> List[UserOut]:
    """
    Retrieves a list of all users.

    Args:
        db (Session): Database session provided by FastAPI (with Depends).

    Returns:
        List[UserOut]: List of users formatted with the output schema.
    """
    return service_user.get_users(db)


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """
    Create a new user.

    Args:
        user (UserCreate): New user data.
        db (Session): Database session.

    Returns:
        UserOut: User created with all fields.
    """
    return service_user.create_user(db, user)
