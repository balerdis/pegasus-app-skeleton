# app/core/database/models/auth/roles_permissions/rol_permission.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from app.core.database.models.base import Base
from pegasus_framework.db.models.auth.roles_permissions.rol_permission_base import BaseRolePermission


class RolePermission(Base, BaseRolePermission):
    __tablename__ = "roles_permissions"

    role_id = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )

    permission_id = mapped_column(
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )