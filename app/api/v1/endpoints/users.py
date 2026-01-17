from fastapi import APIRouter, status, Depends

from app.core.services.dto.user.user_create_dto import UserCreateDTO
from app.core.services.user_service import UserService
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.users.responses import UserResponse
from app.core.services.user_service import UserService
from app.api.dependencies.current_user import get_current_user
from app.core.database.models.users import User


protected_router = APIRouter(
    dependencies=[Depends(get_current_user)]
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

