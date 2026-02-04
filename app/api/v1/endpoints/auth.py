# app/api/v1/auth/login.py
from fastapi import APIRouter, Depends, status, Request
from pegasus_framework.auth.services.auth_service import AuthService

from app.api.v1.schemas.auth.login import LoginRequest
from app.api.v1.schemas.auth.responses import LoginResponse

from app.api.dependencies.auth import get_auth_service, get_bearer_token
from pegasus_framework.auth.dependencies.build_auth_request_context import build_auth_request_context

from app.api.v1.schemas.auth.refresh import RefreshRequest


router = APIRouter()

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    payload: LoginRequest,
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """
    Autentica un usuario y retorna un JWT válido.
    """
    ctx = build_auth_request_context(request=request)
    result = auth_service.login(
        identifier=payload.email,
        password=payload.password,
        context=ctx
    )

    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        expires_at=result.expires_at,
        refresh_token=result.refresh_token,
        refresh_token_expires_at=result.refresh_token_expires_at
    )

@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> None:
    auth_service.logout(access_token=token)

@router.post(
    "/refresh",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def refresh(
    payload: RefreshRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    result = auth_service.refresh(refresh_token=payload.refresh_token)
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        expires_at=result.expires_at,
        refresh_token=result.refresh_token,
        refresh_token_expires_at=result.refresh_token_expires_at
)



