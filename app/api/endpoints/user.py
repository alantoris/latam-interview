from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.user import UserOut, UserCreate
from app.services import user as service_user
from app.services.exceptions import DuplicateUserError


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

    Raises:
        HTTPException: If there is any error in user creation.

    Returns:
        UserOut: User created with all fields.
    """
    try:
        return service_user.create_user(db, user)
    except DuplicateUserError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
