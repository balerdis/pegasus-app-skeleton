# app/core/services/dto/user/user_create_dto.py
from pydantic import Field, EmailStr
from app.core.services.dto.user.user_base import UserBaseDTO
from typing import Optional

class UserCreateDTO(UserBaseDTO):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    name: Optional[str] = Field(None, min_length=2, max_length=255)
    last_name: Optional[str] = Field(None, min_length=2, max_length=255)
    address: Optional[str] = Field(None, min_length=2, max_length=255)

class UserUpdateDTO(UserBaseDTO):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    last_name: Optional[str] = Field(None, min_length=2, max_length=255)
    address: Optional[str] = Field(None, min_length=2, max_length=255)