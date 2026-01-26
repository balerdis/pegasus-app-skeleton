# app/api/dependencies/auth.py
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from pegasus_framework.auth.security.tokens.jwt_token_service import JwtTokenService
from pegasus_framework.auth.security.hash_password import PasswordHasher
from app.config.config import config as settings   
from pegasus_framework.auth.services.auth_service import AuthService


security = HTTPBearer(auto_error=False)

def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación no proporcionadas",
        )
    return credentials.credentials

def get_jwt_token_service() -> JwtTokenService:
    return JwtTokenService(
        secret_key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        access_token_ttl=timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_TTL_MINUTES
        ),        
    )

def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()

def get_auth_service(
    token_service: JwtTokenService = Depends(get_jwt_token_service),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> AuthService:
    return AuthService(
        token_service=token_service,
        password_hasher=password_hasher,
    )

def require_authentication(
    token: str = Depends(get_bearer_token),
    token_service: JwtTokenService = Depends(get_jwt_token_service),
):
    payload = token_service.decode_and_validate(token=token)
    return payload

def require_authenticated_identity(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    return auth_service.authenticate(token=token)






