from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from app.core.database.models.auth.roles_permissions import Role
from sqlalchemy.exc import IntegrityError
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: Session):
        super().__init__(Role, session)

    def create(self, data: dict) -> Role:
        try:
            return super().create(data)
        except IntegrityError as e:
            self.session.rollback()
            if "duplicate entry" in str(e.orig).lower():
                raise DuplicateEntityError(
                    entity="Role",
                    field="code",
                    value=data.get("code"),
                ) from e
            raise
