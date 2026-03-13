from app.core.database.models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from pegasus_framework.db.models.users.user_role_base import BaseUserRole


class UserRole(Base, BaseUserRole):
    __tablename__ = "users_roles"

    user_id = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )

    role_id = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )