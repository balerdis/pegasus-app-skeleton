from sqlalchemy.orm import Session
from pegasus_framework.db.repositories.base_repository import BaseRepository
from app.core.database.models.auth.roles_permissions import Permission
from sqlalchemy.exc import IntegrityError
from pegasus_framework.core.exceptions.domain.duplicate_entry import DuplicateEntityError


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: Session):
        super().__init__(Permission, session)

    def create(self, data: dict) -> Permission:
        try:
            return super().create(data)
        except IntegrityError as e:
            self.session.rollback()
            if "duplicate entry" in str(e.orig).lower():
                raise DuplicateEntityError(
                    entity="Permission",
                    field="code",
                    value=data.get("code"),
                ) from e
            raise
