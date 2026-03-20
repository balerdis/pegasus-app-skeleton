from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService

from app.api.v1.schemas.permissions.create import PermissionCreate
from app.api.v1.schemas.permissions.responses import PermissionResponse
from app.core.database.repositories.permission_repository import PermissionRepository


class PermissionService(SqlAlchemyService):
    def get_all(self) -> list[PermissionResponse]:
        with self._uow() as uow:
            repo = uow.repo(PermissionRepository)
            permissions = repo.get_all()
            return [self._map_permission_to_response(p) for p in permissions]

    def create(self, data: PermissionCreate) -> PermissionResponse:
        with self._uow() as uow:
            repo = uow.repo(PermissionRepository)
            permission = repo.create(data.model_dump())
            uow.commit()
            return self._map_permission_to_response(permission)

    def get_by_id_or_fail(self, id: int) -> PermissionResponse:
        with self._uow() as uow:
            repo = uow.repo(PermissionRepository)
            permission = repo.get_by_id_or_fail(id)
            return self._map_permission_to_response(permission)

    def update(self, id: int, data: PermissionCreate) -> PermissionResponse:
        with self._uow() as uow:
            repo = uow.repo(PermissionRepository)
            permission = repo.get_by_id_or_fail(id)
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(permission, field, value)
            uow.commit()
            return self._map_permission_to_response(permission)

    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        with self._uow() as uow:
            repo = uow.repo(PermissionRepository)
            if confirm:
                repo.delete_by_id(id, confirm)
                uow.commit()

    def _map_permission_to_response(self, p) -> PermissionResponse:
        return PermissionResponse(
            id=p.id,
            code=p.code,
            description=p.description
        )
