from fastapi import status, APIRouter
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.permissions.responses import PermissionResponse, DeletePermissionResponse
from app.api.v1.schemas.permissions.create import PermissionCreate
from app.core.services.permission_service import PermissionService

router = APIRouter()


@router.post("/",
            response_model=ApiResponse[PermissionResponse],
            description="Crea un nuevo permiso",
            status_code=status.HTTP_201_CREATED
            )
def create_permission(request: PermissionCreate):
    service = PermissionService()
    permission = service.create(request)

    return ApiResponse(
        status="success",
        message="Permiso creado correctamente",
        errors=[],
        data=PermissionResponse.model_validate(permission)
    )


@router.get("/",
            response_model=ApiResponse[list[PermissionResponse]],
            description="Devuelve todos los permisos",
            status_code=status.HTTP_200_OK
            )
def get_permissions():
    service = PermissionService()
    permissions = service.get_all()

    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[PermissionResponse.model_validate(p) for p in permissions]
    )


@router.get("/{permission_id}",
            response_model=ApiResponse[PermissionResponse],
            description="Devuelve un permiso por id",
            status_code=status.HTTP_200_OK
            )
def get_by_id(permission_id: int):
    service = PermissionService()
    permission = service.get_by_id_or_fail(permission_id)

    return ApiResponse(
        status="success",
        message="Permiso obtenido correctamente",
        errors=[],
        data=PermissionResponse.model_validate(permission)
    )


@router.patch("/{permission_id}",
            response_model=ApiResponse[PermissionResponse],
            description="Actualiza un permiso",
            status_code=status.HTTP_200_OK
            )
def update_by_id(permission_id: int, request: PermissionCreate):
    service = PermissionService()
    permission_updated = service.update(permission_id, request)

    return ApiResponse(
        status="success",
        message="Permiso actualizado correctamente",
        errors=[],
        data=PermissionResponse.model_validate(permission_updated)
    )


@router.delete("/{permission_id}",
            response_model=ApiResponse[DeletePermissionResponse],
            description="Elimina un permiso",
            status_code=status.HTTP_200_OK
            )
def delete_by_id(permission_id: int, confirm: bool = True):
    service = PermissionService()
    service.delete_by_id(permission_id, confirm)

    return ApiResponse(
        status="success",
        message="Permiso eliminado correctamente",
        errors=[],
        data=DeletePermissionResponse(permission_id=permission_id)
    )
