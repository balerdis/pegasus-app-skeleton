# app/api/v1/schemas/users/responses.py

from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    habilited: bool

class DeleteUserResponse(BaseModel):
    id: int