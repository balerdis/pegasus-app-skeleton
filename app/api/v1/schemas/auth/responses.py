# app/api/v1/schemas/auth/responses.py
from pydantic import BaseModel
from datetime import datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime

