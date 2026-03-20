from pegasus_framework.business.sqlalchemy_service import SqlAlchemyService

from app.api.v1.schemas.roles.create import RoleCreate, RoleUpdate
from app.api.v1.schemas.roles.responses import RoleResponse, PermissionBrief
from app.core.database.repositories.role_repository import RoleRepository
from app.core.database.repositories.permission_repository import PermissionRepository


class RoleService(SqlAlchemyService):
    def get_all(self) -> list[RoleResponse]:
        with self._uow() as uow:
            repo = uow.repo(RoleRepository)
            roles = repo.get_all()
            return [self._map_role_to_response(r) for r in roles]

    def create(self, data: RoleCreate) -> RoleResponse:
        with self._uow() as uow:
            role_repo = uow.repo(RoleRepository)
            permission_repo = uow.repo(PermissionRepository)

            role_data = {"code": data.code, "description": data.description}
            role = role_repo.create(role_data)

            for perm_id in data.permission_ids:
                permission = permission_repo.get_by_id_or_fail(perm_id)
                role.permissions.append(permission)

            uow.commit()
            return self._map_role_to_response(role)

    def get_by_id_or_fail(self, id: int) -> RoleResponse:
        with self._uow() as uow:
            repo = uow.repo(RoleRepository)
            role = repo.get_by_id_or_fail(id)
            return self._map_role_to_response(role)

    def update(self, id: int, data: RoleUpdate) -> RoleResponse:
        with self._uow() as uow:
            role_repo = uow.repo(RoleRepository)
            permission_repo = uow.repo(PermissionRepository)

            role = role_repo.get_by_id_or_fail(id)

            update_data = data.model_dump(exclude_unset=True, exclude={"permission_ids"})
            for field, value in update_data.items():
                if value is not None:
                    setattr(role, field, value)

            if data.permission_ids is not None:
                role.permissions.clear()
                for perm_id in data.permission_ids:
                    permission = permission_repo.get_by_id_or_fail(perm_id)
                    role.permissions.append(permission)

            uow.commit()
            return self._map_role_to_response(role)

    def delete_by_id(self, id: int, confirm: bool = True) -> None:
        with self._uow() as uow:
            repo = uow.repo(RoleRepository)
            if confirm:
                repo.delete_by_id(id, confirm)
                uow.commit()

    def _map_role_to_response(self, r) -> RoleResponse:
        return RoleResponse(
            id=r.id,
            code=r.code,
            description=r.description,
            permissions=[
                PermissionBrief(id=p.id, code=p.code) for p in r.permissions
            ] if r.permissions else []
        )
