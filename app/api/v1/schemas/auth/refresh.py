# app/api/v1/schemas/auth/refresh.py
from pydantic import BaseModel

class RefreshRequest(BaseModel):
    refresh_token: str