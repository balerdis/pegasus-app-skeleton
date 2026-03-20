from pydantic import BaseModel


class PermissionBrief(BaseModel):
    id: int
    code: str

    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    id: int
    code: str
    description: str | None
    permissions: list[PermissionBrief] = []

    class Config:
        from_attributes = True


class RoleBriefResponse(BaseModel):
    id: int
    code: str

    class Config:
        from_attributes = True


class DeleteRoleResponse(BaseModel):
    role_id: int
