from fastapi import APIRouter, Depends, status

from pegasus_framework.business.users.dto import UserCreateDTO
from pegasus_framework.business.users.user_service import UserService
from pegasus_framework.api.v1.schemas.generic import ApiResponse
from pegasus_framework.wiring.bootstrap import get_user_service
from app.api.v1.schemas.users.responses import UserResponse

router = APIRouter()


@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserCreateDTO,
    service: UserService = Depends(get_user_service),
):
    user = service.create_user(request)

    return ApiResponse(
        status="success",
        message="El usuario fue creado correctamente",
        errors=[],
        data=user,
    )
