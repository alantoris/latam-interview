import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped
from app.db import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(Base):
    """
    User model representing a user record in the database.

    Attributes:
    - id (UUID): Unique identifier for the user, generated automatically.
    - username (str): Unique username for login and identification.
    - email (str): Unique email address of the user.
    - first_name (str): User's first name.
    - last_name (str): User's last name.
    - role (str): User role, e.g. 'admin', 'user', 'guest'.
    - created_at (datetime): Timestamp when the user was created (UTC).
    - updated_at (datetime): Timestamp when the user was last updated (UTC).
    - active (bool): Flag indicating whether the user account is active.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
        doc="Unique UUID identifier for the user",
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="userrole_enum"),
        nullable=False,
        doc="Role of the user (e.g., admin, user, guest)",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
