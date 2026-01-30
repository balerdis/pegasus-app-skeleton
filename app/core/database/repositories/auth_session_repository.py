# app/core/database/repositories/auth_session_repository.py
from pegasus_framework.db.repositories.auth.sessions.auth_session_repository_base import AuthSessionRepositoryBase
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from pegasus_framework.auth.context.auth_request_context import AuthRequestContext

from app.core.database.models.auth.auth_session import AuthSession
class AuthSessionRepository(AuthSessionRepositoryBase):
    """
    Implementación concreta del AuthSessionRepositoryBase usando SQLAlchemy.

    - ORM-aware
    - Usa soft delete indirectamente solo si el modelo lo define
    - Respeta todas las invariantes del contrato
    """

    def __init__(self, session: Session):
        self.session = session


    def create(
        self,
        *,
        status: str = "active",
        last_activity_at: datetime,
        expires_at: datetime,
        user_id: int,
        context: AuthRequestContext | None = None
    ) -> AuthSession:
        session = AuthSession(
            status=status,
            last_activity_at=last_activity_at,
            expires_at=expires_at,
            ip_address=context.ip_address,
            user_agent=context.user_agent,
            accept_language=context.accept_language,
            user_id=user_id
        )

        self.session.add(session)
        self.session.flush()

        return session   
    
    def get_valid_by_token_id(
        self,
        *,
        token_id: str,
        now: datetime,
    ) -> AuthSession:
        return self.session.scalar(
            select(AuthSession).where(AuthSession.token_id == token_id).where(AuthSession.expires_at > now)
        )
    
    def revoke(self, 
               access_token_jti: str, 
               revoked_at: datetime
               ):
        self.session.execute(
            update(AuthSession).where(AuthSession.token_jti == access_token_jti).values(revoked_at=revoked_at)
        )
        self.session.flush()

        return

    def revoke_all_for_user(self, *, user_id, revoked_at: datetime):
        self.session.execute(
            update(AuthSession).where(AuthSession.user_id == user_id).values(revoked_at=revoked_at)
        )
        self.session.flush()

        return
