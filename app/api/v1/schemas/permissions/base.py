from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=255)
