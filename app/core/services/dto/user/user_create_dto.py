from pydantic import Field
from app.core.services.dto.user.user_base import UserBaseDTO

class UserCreateDTO(UserBaseDTO):
    password: str = Field(..., min_length=8, max_length=128)