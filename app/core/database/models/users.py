# app/core/database/models/users.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.models.base import Base
from pegasus_framework.db.models.users.user_base import BaseUser
from pegasus_framework.db.models.users.mixins import AuditableUserMixin
from pegasus_framework.db.models.mixins import AuditMixin
from sqlalchemy.orm import relationship

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


    sessions = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )    
