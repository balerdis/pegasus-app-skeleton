# app/wiring/repositories/session_repository.py
from pegasus_framework.auth.repositories.sessions.session_repository import (
    SessionRepository,
)
from app.core.database.repositories.session_repository import (
    SqlAlchemySessionRepository,
)

REPOSITORY_BINDINGS = {
    SessionRepository: SqlAlchemySessionRepository,
}
