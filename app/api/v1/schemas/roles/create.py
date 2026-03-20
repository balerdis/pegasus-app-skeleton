from pydantic import BaseModel, Field
from typing import List, Optional


class RoleBase(BaseModel):
    code: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None, max_length=255)


class RoleCreate(RoleBase):
    permission_ids: List[int] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    permission_ids: Optional[List[int]] = None
