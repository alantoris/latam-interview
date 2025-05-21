from pydantic import BaseModel, EmailStr, constr
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """
    Contains common fields between user input and output.
    Applies basic validation with Pydantic.
    """

    username: constr(strip_whitespace=True, min_length=3, max_length=50)
    email: EmailStr
    first_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    last_name: constr(strip_whitespace=True, min_length=1, max_length=50)
    role: constr(strip_whitespace=True, min_length=2, max_length=20)


class UserCreate(UserBase):
    """
    Represents the body of a POST to create users.
    Inherits all validations from UserBase.
    """

    pass


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
