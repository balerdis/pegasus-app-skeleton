# app/api/v1/schemas/auth/login.py
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=8, description="Password en texto plano")

    class Config:
        schema_extra = {
            "example": {
                "email": "8tHsL@example.com",
                "password": "password123",
            }
        }