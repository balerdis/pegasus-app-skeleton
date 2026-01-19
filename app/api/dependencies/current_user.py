from fastapi import Depends, HTTPException, status

from app.api.dependencies.auth import get_bearer_token, get_auth_service
from app.api.dependencies.users import get_user_service
from app.core.services import auth
from app.core.services.auth.auth_service import AuthService
from app.core.services.user_service import UserService
from app.core.database.models.users import User

def get_current_user(
    token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(get_auth_service),
    user_service: UserService = Depends(get_user_service),
) -> User:
    user_id = auth_service.authenticate(token=token)
    return user_service.get_user_by_id(user_id)
