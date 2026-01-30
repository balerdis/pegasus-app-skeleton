# app/wiring/repositories/bindings.py

from pegasus_framework.db.repositories.auth.sessions.auth_session_repository_base import AuthSessionRepositoryBase
from pegasus_framework.db.repositories.auth.sessions.auth_session_token_repository_base import AuthSessionTokenRepositoryBase

from app.core.database.repositories.auth_session_repository import AuthSessionRepository
from app.core.database.repositories.auth_session_token_repository import AuthSessionTokenRepository

REPOSITORY_BINDINGS = {
    AuthSessionRepositoryBase: AuthSessionRepository,
    AuthSessionTokenRepositoryBase: AuthSessionTokenRepository
}