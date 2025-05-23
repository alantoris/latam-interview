import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi_pagination import Page, Params

from app.db import get_db
from app.schemas.user import UserOut, UserCreate, UserUpdate, UserPartialUpdate
from app.services import user as service_user
from app.services.exceptions import DuplicateUserError

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.get("/{user_id}", response_model=UserOut)
def retrieve_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOut:
    """
    Retrieves a specific user.

    Args:
        user_id: Query param UUID from the user to retrieve.
        db (Session): Database session provided by FastAPI (with Depends).

    Raises:
        HTTPException: If the user does not exists.

    Returns:
        UserOut: User formatted with the output schema.
    """
    logger.info(f"Retrieving user with ID: {user_id}")
    try:
        return service_user.get_user_by_id(db, user_id)
    except NoResultFound:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=Page[UserOut])
def list_users(
    db: Session = Depends(get_db), params: Params = Depends()
) -> Page[UserOut]:
    """
    Retrieves a list of all users.

    Args:
        db (Session): Database session provided by FastAPI (with Depends).

    Returns:
        Page[UserOut]: List of users paginated formatted with the output schema.
    """
    logger.info("Listing all users")
    return service_user.get_users(db, params)


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
    logger.info(f"Creating user with email: {user.email}")
    try:
        return service_user.create_user(db, user)
    except DuplicateUserError as e:
        logger.error(f"Failed to create user: duplicate email {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: UUID, user_in: UserUpdate, db: Session = Depends(get_db)
) -> UserOut:
    """
    Update a user.

    Args:
        user_id: Query param UUID from the user to update.
        user_in (UserUpdate): Updated user data.
        db (Session): Database session.

    Raises:
        HTTPException: If there is any error in user update or if the user does not exists.

    Returns:
        UserOut: User created with all fields.
    """
    logger.info(f"Updating user {user_id}")
    try:
        return service_user.update_user(db, user_id, user_in)
    except NoResultFound:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateUserError as e:
        logger.error(f"Failed to update user {user_id}: duplicate email")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{user_id}", response_model=UserOut)
def partial_update_user(
    user_id: UUID, user_in: UserPartialUpdate, db: Session = Depends(get_db)
) -> UserOut:
    """
    Partialy update a user.

    Args:
        user_id: Query param UUID from the user to update partially.
        user_in (UserPartialUpdate): Updated user data.
        db (Session): Database session.

    Raises:
        HTTPException: If there is any error in user update or if the user does not exists.

    Returns:
        UserOut: User created with all fields.
    """
    logger.info(f"Partially updating user {user_id}")
    try:
        return service_user.update_user(db, user_id, user_in)
    except NoResultFound:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    except DuplicateUserError as e:
        logger.error(f"Failed to partially update user {user_id}: duplicate email")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> None:
    """
    Delete a user.

    Args:
        user_id: Query param UUID from the user to delete.
        db (Session): Database session.

    Raises:
        HTTPException: If the user does not exists.
    """
    logger.info(f"Deleting user {user_id}")
    try:
        service_user.delete_user(db, user_id)
        logger.info(f"Successfully deleted user {user_id}")
    except NoResultFound:
        logger.error(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
