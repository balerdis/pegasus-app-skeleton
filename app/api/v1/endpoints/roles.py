from fastapi import status, APIRouter
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.roles.responses import RoleResponse, DeleteRoleResponse
from app.api.v1.schemas.roles.create import RoleCreate, RoleUpdate
from app.core.services.role_service import RoleService

router = APIRouter()


@router.post("/",
            response_model=ApiResponse[RoleResponse],
            description="Crea un nuevo rol",
            status_code=status.HTTP_201_CREATED
            )
def create_role(request: RoleCreate):
    service = RoleService()
    role = service.create(request)

    return ApiResponse(
        status="success",
        message="Rol creado correctamente",
        errors=[],
        data=RoleResponse.model_validate(role)
    )


@router.get("/",
            response_model=ApiResponse[list[RoleResponse]],
            description="Devuelve todos los roles",
            status_code=status.HTTP_200_OK
            )
def get_roles():
    service = RoleService()
    roles = service.get_all()

    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[RoleResponse.model_validate(r) for r in roles]
    )


@router.get("/{role_id}",
            response_model=ApiResponse[RoleResponse],
            description="Devuelve un rol por id",
            status_code=status.HTTP_200_OK
            )
def get_by_id(role_id: int):
    service = RoleService()
    role = service.get_by_id_or_fail(role_id)

    return ApiResponse(
        status="success",
        message="Rol obtenido correctamente",
        errors=[],
        data=RoleResponse.model_validate(role)
    )


@router.patch("/{role_id}",
            response_model=ApiResponse[RoleResponse],
            description="Actualiza un rol",
            status_code=status.HTTP_200_OK
            )
def update_by_id(role_id: int, request: RoleUpdate):
    service = RoleService()
    role_updated = service.update(role_id, request)

    return ApiResponse(
        status="success",
        message="Rol actualizado correctamente",
        errors=[],
        data=RoleResponse.model_validate(role_updated)
    )


@router.delete("/{role_id}",
            response_model=ApiResponse[DeleteRoleResponse],
            description="Elimina un rol",
            status_code=status.HTTP_200_OK
            )
def delete_by_id(role_id: int, confirm: bool = True):
    service = RoleService()
    service.delete_by_id(role_id, confirm)

    return ApiResponse(
        status="success",
        message="Rol eliminado correctamente",
        errors=[],
        data=DeleteRoleResponse(role_id=role_id)
    )
