# app/api/v1/schemas/users/responses.py

from pydantic import BaseModel


class RoleBrief(BaseModel):
    id: int
    code: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    habilited: bool
    roles: list[RoleBrief] = []

    class Config:
        from_attributes = True


class DeleteUserResponse(BaseModel):
    id: int


class UserRolesResponse(BaseModel):
    id: int
    email: str
    name: str
    roles: list[RoleBrief] = []

    class Config:
        from_attributes = True