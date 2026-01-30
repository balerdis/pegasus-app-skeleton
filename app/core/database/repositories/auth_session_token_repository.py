# app/core/database/repositories/auth_session_token_repository.py
from pegasus_framework.db.repositories.auth.sessions.auth_session_token_repository_base import (
    AuthSessionTokenRepositoryBase
)
from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.core.database.models.auth.auth_session_token import AuthSessionToken
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
    
    def revoke(self, *, 
               token_id: str, 
               revoked_at: datetime
               ):
        self.session.execute(
            update(AuthSessionToken).where(AuthSessionToken.token_id == token_id).values(revoked_at=revoked_at)
        )
        self.session.flush()

        return
    
    def get_valid_by_token_id(self, *, 
                              token_id: str, 
                              now: datetime
                              ):
        return self.session.scalar(
            select(AuthSessionToken).where(AuthSessionToken.token_id == token_id).where(AuthSessionToken.expires_at > now)
        )
    
    def get_valid_by_refresh_token_id(self, *, 
                                      token_id: str, 
                                      now: datetime
                                      ):
        return self.session.scalar(
            select(AuthSessionToken).where(AuthSessionToken.token_id == token_id).where(AuthSessionToken.expires_at > now)
        )
    
    def get_valid_by_access_token_id(self, *, 
                                     token_id: str, 
                                     now: datetime
                                     ):
        return self.session.scalar(
            select(AuthSessionToken).where(AuthSessionToken.token_id == token_id).where(AuthSessionToken.expires_at > now)
        )
    
    def get_all_by_user_id(self, 
                           *, 
                           user_id: int
                           ):
        return self.session.scalars(
            select(AuthSessionToken).where(AuthSessionToken.user_id == user_id)
        ).all()
    
    def get_all_by_token_type_and_user_id(self, 
                                          *, 
                                          token_type: TokenType, 
                                          user_id: int
                                          ):
        return self.session.scalars(
            select(AuthSessionToken).where(AuthSessionToken.token_type == token_type.value).where(AuthSessionToken.user_id == user_id)
        ).all()