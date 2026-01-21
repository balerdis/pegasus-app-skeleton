# app/api/v1/auth/login.py
from fastapi import APIRouter, Depends, status

from app.api.v1.schemas.auth.login import LoginRequest
from app.api.v1.schemas.auth.responses import LoginResponse

from app.core.services.auth.auth_service import AuthService
from app.api.dependencies.auth import get_auth_service, get_bearer_token



router = APIRouter()

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """
    Autentica un usuario y retorna un JWT válido.
    """

    result = auth_service.login(
        identifier=payload.email,
        password=payload.password,
    )

    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        expires_at=result.expires_at,
    )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    auth_service.logout(token=token)



