# app/core/database/models/user_session.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.base import Base
from app.core.database.models.users import User
from pegasus_framework.auth.models.sessions.user_session_base import UserSessionBase

class UserSession(Base, UserSessionBase):
    __tablename__ = "user_sessions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="sessions"
    )

    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id})>"