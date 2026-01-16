from datetime import datetime

from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService

from app.core.database.repositories.session_repository import (
    SqlAlchemySessionRepository,
)


class AuthSessionService(SqlAlchemyService):
    """
    Servicio de dominio técnico para la gestión de sesiones de autenticación.

    - Usa Unit of Work
    - No conoce HTTP
    - No conoce JWT
    - Orquesta reglas sobre sesiones persistentes
    """

    def create_session(
        self,
        *,
        user_id: int,
        token_id: str,
        expires_at: datetime,
    ):
        """
        Crea una nueva sesión para un usuario.
        """
        with self._uow() as uow:
            repo = uow.repo(SqlAlchemySessionRepository)

            session = repo.create(
                user_id=user_id,
                token_id=token_id,
                expires_at=expires_at,
            )

            uow.commit()
            return session

    def get_valid_session(
        self,
        *,
        token_id: str,
        now: datetime,
    ):
        """
        Retorna la sesión válida asociada al token_id o None.
        """
        with self._uow() as uow:
            repo = uow.repo(SqlAlchemySessionRepository)

            return repo.get_valid_by_token_id(
                token_id=token_id,
                now=now,
            )

    def revoke_session(
        self,
        *,
        token_id: str,
    ) -> None:
        """
        Revoca una sesión específica por token_id.
        """
        with self._uow() as uow:
            repo = uow.repo(SqlAlchemySessionRepository)

            repo.revoke(token_id=token_id)

            uow.commit()

    def revoke_all_sessions_for_user(
        self,
        *,
        user_id: int,
    ) -> int:
        """
        Revoca todas las sesiones activas de un usuario.
        """
        with self._uow() as uow:
            repo = uow.repo(SqlAlchemySessionRepository)

            count = repo.revoke_all_for_user(user_id=user_id)

            uow.commit()
            return count
