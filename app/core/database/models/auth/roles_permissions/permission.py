# app/core/database/models/auth/roles_permissions/permission.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from app.core.database.models.base import Base
from pegasus_framework.db.models.auth.roles_permissions.permission_base import BasePermission
from pegasus_framework.db.models.mixins import AuditMixin

if TYPE_CHECKING:
    from app.core.database.models.auth.roles_permissions.role import Role

class Permission(AuditMixin, Base, BasePermission):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="roles_permissions",
        back_populates="permissions"
    )