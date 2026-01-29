# app/core/database/models/auth/auth_session.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.auth.auth_session import AuthSession
from pegasus_framework.db.models.auth.session.auth_session_tokens_base import AuthSessionTokensBase

class AuthSessionToken(Base, AuthSessionTokensBase):
    __tablename__ = "auth_session_tokens"

    auth_session_id: Mapped[int] = mapped_column(
        ForeignKey("auth_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    auth_session: Mapped["AuthSession"] = relationship(
        "AuthSession",
        back_populates="tokens"
    )

    def __repr__(self):
        return f"<AuthSessionToken(id={self.id}, auth_session_id={self.auth_session_id})>"