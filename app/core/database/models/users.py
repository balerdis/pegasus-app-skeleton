# app/core/database/models/users.py
from __future__ import annotations
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from app.core.database.models.base import Base
from pegasus_framework.db.models.users.user_base import BaseUser
from pegasus_framework.db.models.users.mixins import AuditableUserMixin
from pegasus_framework.db.models.mixins import AuditMixin

if TYPE_CHECKING:
    from app.core.database.models.auth.roles_permissions.role import Role

class User(
    AuditMixin,
    Base,
    BaseUser,
    AuditableUserMixin,
):
    """Este modelo utiliza como base el contrato establecido por el framework (ver dependencias / herencia)

    Args:
        BaseUser (_type_): Contrato establecido por el framework
        AuditableUserMixin (_type_): Contratos opcionales establecidos por el framework
    """
    __tablename__ = "users"

    display_name: Mapped[str | None] = mapped_column(String(120))

    roles: Mapped[List[Role]] = relationship(
        "Role",
        secondary="users_roles",
        back_populates="users"
    )

