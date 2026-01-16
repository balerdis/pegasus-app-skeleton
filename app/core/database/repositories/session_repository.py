# app/core/database/repositories/session_repository.py
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from pegasus_framework.auth.repositories.sessions.session_repository import (
    SessionRepository,
)

from app.core.database.models.user_sessions import UserSession


class SqlAlchemySessionRepository(SessionRepository):
    """
    Implementación concreta del SessionRepository usando SQLAlchemy.

    - ORM-aware
    - Usa soft delete indirectamente solo si el modelo lo define
    - Respeta todas las invariantes del contrato
    """

    def __init__(self, session: Session):
        self.session = session

    def create(
        self,
        *,
        user_id: int,
        token_id: str,
        expires_at: datetime,
    ) -> UserSession:
        session = UserSession(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
            is_revoked=False,
        )

        self.session.add(session)
        self.session.flush()

        return session

    def get_valid_by_token_id(
        self,
        *,
        token_id: str,
        now: datetime,
    ) -> Optional[UserSession]:
        stmt = (
            select(UserSession)
            .where(
                UserSession.token_id == token_id,
                UserSession.is_revoked.is_(False),
                UserSession.expires_at > now,
            )
        )

        return self.session.execute(stmt).scalar_one_or_none()

    def revoke(
        self,
        *,
        token_id: str,
        revoked_at: Optional[datetime] = None,
    ) -> None:
        """
        Revocación idempotente.

        Si la sesión no existe o ya está revocada, no falla.
        """
        stmt = (
            update(UserSession)
            .where(
                UserSession.token_id == token_id,
                UserSession.is_revoked.is_(False),
            )
            .values(is_revoked=True)
        )

        self.session.execute(stmt)
        self.session.flush()

    def revoke_all_for_user(
        self,
        *,
        user_id: int,
    ) -> int:
        stmt = (
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.is_revoked.is_(False),
            )
            .values(is_revoked=True)
        )

        result = self.session.execute(stmt)
        self.session.flush()

        return result.rowcount or 0
