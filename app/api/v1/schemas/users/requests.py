# app/api/v1/schemas/users/requests.py

from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    name: str
    last_name: str
    address: str
    email: EmailStr
    password: str
