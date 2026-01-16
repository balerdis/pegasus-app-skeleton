from fastapi import APIRouter, status

from app.core.services.dto.user.user_create_dto import UserCreateDTO
from app.core.services.user_service import UserService
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from app.api.v1.schemas.users.responses import UserResponse
from app.core.services.user_service import UserService

router = APIRouter()


@router.post(
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
