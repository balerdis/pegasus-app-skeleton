from fastapi import APIRouter, status, Depends

from app.core.services.dto.user.user_create_dto import UserCreateDTO, UserUpdateDTO
from app.core.services.user_service import UserService
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.users.responses import UserResponse, DeleteUserResponse
from app.core.services.user_service import UserService
from app.api.dependencies.auth import require_authentication
from app.api.dependencies.current_user import get_current_user
from app.core.database.models.users import User


protected_router = APIRouter(
    dependencies=[Depends(require_authentication)]
)


@protected_router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserCreateDTO
):
    service = UserService()
    user = service.create_user(request)

    return ApiResponse(
        status="success",
        message="El usuario fue creado correctamente",
        errors=[],
        data=user,
    )

@protected_router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }

# ###################GET ALL USERS###################
@protected_router.get("/", 
            response_model=ApiResponse[list[UserResponse]],
            description="Devuelve todos los users",
            status_code=status.HTTP_200_OK
            )
def get_users():
    service = UserService()
    users = service.get_all()
        
    return ApiResponse(
        status="success",
        message="Listado obtenido correctamente",
        errors=[],
        data=[UserResponse.model_validate(u) for u in users]
    )

# ###################GET USER BY ID###################
@protected_router.get("/{id}", 
            response_model=ApiResponse[UserResponse],
            description="Devuelve un genero por id",
            status_code=status.HTTP_200_OK
            )
def get_by_id(id: int):
    service = UserService()
    entity = service.get_by_id_or_fail(id)

    return ApiResponse(
        status="success",
        message="Usuario obtenido correctamente",
        errors=[],
        data=UserResponse.model_validate(entity)
    )

# ####################UPDATE USER###################
@protected_router.patch("/{id}", 
            response_model=ApiResponse[UserResponse],
            description="Actualiza un genero",
            status_code=status.HTTP_200_OK
            )
def update_by_id(
    id: int, 
    request: UserUpdateDTO,
):
    service = UserService()
    updated = service.update(id, request)

    return ApiResponse(
        status="success",
        message="Genero actualizado correctamente",
        errors=[],
        data=UserResponse.model_validate(updated)
    )

# ####################DELETE USER###################
@protected_router.delete("/{id}", 
            response_model=ApiResponse[DeleteUserResponse],
            description="Elimina un genero",
            status_code=status.HTTP_200_OK
            )
def delete_by_id(
    id: int, 
    confirm: bool = True
):
    service = UserService()
    service.delete_by_id(id, confirm)

    return ApiResponse(
        status="success",
        message="Genero eliminado correctamente",
        errors=[],
        data=DeleteUserResponse(id=id)
    )



