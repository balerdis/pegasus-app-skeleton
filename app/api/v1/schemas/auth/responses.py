# app/api/v1/schemas/auth/responses.py
from pydantic import BaseModel
from datetime import datetime
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LoginResult:
    access_token: str
    token_type: str
    expires_at: datetime
    

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime

