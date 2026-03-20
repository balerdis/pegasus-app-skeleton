# app/core/database/models/auth/roles_permissions/role.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from app.core.database.models.base import Base

from pegasus_framework.db.models.auth.roles_permissions.rol_base import BaseRole
from pegasus_framework.db.models.mixins import AuditMixin

if TYPE_CHECKING:
    from app.core.database.models.auth.roles_permissions.permission import Permission
    from app.core.database.models.users import User

class Role(AuditMixin, Base, BaseRole):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    permissions: Mapped[List["Permission"]] = relationship( 
        "Permission", secondary="roles_permissions", back_populates="roles"
    )
    users: Mapped[List["User"]] = relationship( 
        "User", secondary="users_roles", back_populates="roles"
    )