# app/api/dependencies/auth.py
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from pegasus_framework.auth.security.tokens.jwt_token_service import JwtTokenService
from pegasus_framework.auth.security.hash_password import PasswordHasher
from app.config.config import config as settings   
from app.core.services.auth.auth_service import AuthService
from app.api.v1.schemas import status

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

def get_auth_service() -> AuthService:
    return AuthService(
        token_service=JwtTokenService(
            secret_key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        ),
        password_hasher=PasswordHasher(),
        access_token_ttl=timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_TTL_MINUTES
        ),
    )



