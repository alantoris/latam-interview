from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr
from uuid import UUID

from app.models.user import UserRole


class UserBase(BaseModel):
    """
    Contains common fields between user input and output.
    Applies basic validation with Pydantic.
    """

    username: constr(strip_whitespace=True, min_length=3, max_length=50)
    email: EmailStr
    first_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    role: UserRole
    active: bool = False


class UserCreate(UserBase):
    """
    Represents the body of a POST to create users.
    Inherits all validations from UserBase.
    """

    pass


class UserUpdate(UserBase):
    """
    Represents the body of a PUT to update users.
    Inherits all validations from UserBase.
    """

    pass


class UserPartialUpdate(UserBase):
    """
    Schema for updating an existing user.
    All fields are optional for partial updates.
    """

    username: Optional[
        constr(strip_whitespace=True, min_length=3, max_length=50)
    ] = None
    email: Optional[EmailStr] = None
    first_name: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=50)
    ] = None
    last_name: Optional[
        constr(strip_whitespace=True, min_length=1, max_length=50)
    ] = None
    role: Optional[UserRole] = None
    active: Optional[bool] = None


class UserOut(UserBase):
    """
    Represents the response returned when listing or creating users.
    Includes additional metadata and allows conversion from ORMs.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime
    active: bool

    model_config = {"from_attributes": True}
