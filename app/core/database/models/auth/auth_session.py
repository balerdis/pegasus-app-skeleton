# app/core/database/models/auth/auth_session.py
from app.core.database.models.base import Base
from pegasus_framework.db.models.auth.session.auth_session_base import AuthSessionBase
from pegasus_framework.db.models.mixins import AuditMixin
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

class AuthSession(
    AuditMixin,
    Base,
    AuthSessionBase,
):
    """Este modelo utiliza como base el contrato establecido por el framework (ver dependencias / herencia)

    Args:
        AuthSessionBase: Contrato establecido por el framework
        AuditMixin: Contratos opcionales establecidos por el framework
    """
    __tablename__ = "auth_sessions"

    sessions = relationship(
        "AuthSessionToken",
        back_populates="auth_session",
        cascade="all, delete-orphan"
    )    

    tokens = relationship(
        "AuthSessionToken",
        back_populates="auth_session",
        cascade="all, delete-orphan"
    )    

    user_id : Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    def __repr__(self):
        return f"<AuthSession(id={self.id}, user_id={self.user_id})>"
