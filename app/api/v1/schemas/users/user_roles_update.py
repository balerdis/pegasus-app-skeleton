# app/api/v1/schemas/users/user_roles_update.py
from pydantic import BaseModel, Field
from typing import List


class UserRolesUpdateRequest(BaseModel):
    role_ids: List[int] = Field(..., description="Lista de IDs de roles a asignar al usuario")
