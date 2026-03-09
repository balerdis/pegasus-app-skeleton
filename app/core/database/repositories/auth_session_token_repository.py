# app/core/database/repositories/auth_session_token_repository.py
from pegasus_framework.db.repositories.auth.sessions.auth_session_token_repository_base import (
    AuthSessionTokenRepositoryBase
)
from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database.models.auth.sessions.auth_session_token import AuthSessionToken
from pegasus_framework.db.repositories.base_repository import BaseRepository
from pegasus_framework.business.domain.auth.token_type import TokenType

class AuthSessionTokenRepository(AuthSessionTokenRepositoryBase, BaseRepository[AuthSessionToken]):

    def __init__(self, session: Session):
        super().__init__(AuthSessionToken, session)

    def create(self,
               auth_session_id: int,
               token_jti: str, 
               token_type: str,
               issued_at: datetime,
               expires_at: datetime | None = None,
               replaced_by_token: Optional[int] = None,
               extra_data: Optional[Dict[str, Any]] = None
               ):
        session = AuthSessionToken(
            auth_session_id=auth_session_id,
            token_jti=token_jti,
            token_type=token_type,
            issued_at=issued_at,
            expires_at=expires_at,
            replaced_by_token=replaced_by_token,
            extra_data=extra_data,
        )

        self.session.add(session)
        self.session.flush()

        return session
    
    def revoke_by_auth_session_id(self, *, 
                                  auth_session_id: int, 
                                  revoked_at: datetime
                                  ):
        self.session.execute(
            update(AuthSessionToken).where(AuthSessionToken.auth_session_id == auth_session_id).values(revoked_at=revoked_at)
        )
        self.session.flush()

        return
    
       
    
    def get_valid_access_token(
        self,
        *,
        token_jti: str,
        now: datetime,
    ) -> AuthSessionToken | None:
        return self.session.scalar(
            select(AuthSessionToken)
            .where(AuthSessionToken.token_jti == token_jti)
            .where(AuthSessionToken.token_type == TokenType.ACCESS.value)
            .where(AuthSessionToken.expires_at > now)
            .where(AuthSessionToken.revoked_at.is_(None))
        )    
    
    def get_valid_refresh_token(
        self,
        *,
        token_jti: str,
        now: datetime,
    ) -> AuthSessionToken | None:
        return self.session.scalar(
            select(AuthSessionToken)
            .where(AuthSessionToken.token_jti == token_jti)
            .where(AuthSessionToken.token_type == TokenType.REFRESH.value)
            .where(AuthSessionToken.expires_at > now)
            .where(AuthSessionToken.revoked_at.is_(None))
        )
    
    def get_valid_by_token_jti(
        self,
        *,
        token_jti: str,
        now: datetime,
        token_type: str
    ) -> AuthSessionToken | None:
        return self.session.scalar(
            select(AuthSessionToken)
            .where(AuthSessionToken.token_jti == token_jti)
            .where(AuthSessionToken.expires_at > now)
            .where(AuthSessionToken.revoked_at.is_(None))
            .where(AuthSessionToken.token_type == token_type)
        )

    def update_refresh_token_replaced_by(
        self,
        *,
        refresh_token_jti: str,
        replaced_by_token_jti: str,
    ) -> None:
        self.session.execute(
            update(AuthSessionToken).where(AuthSessionToken.token_jti == refresh_token_jti).values(replaced_by_token=replaced_by_token_jti)
        )
        self.session.flush()

    def revoke_by_token_jti(self, 
           token_jti: str, 
           revoked_at: datetime
           ):
        self.session.execute(
            update(AuthSessionToken).where(AuthSessionToken.token_jti == token_jti).values(revoked_at=revoked_at)
        )
        self.session.flush()

        return