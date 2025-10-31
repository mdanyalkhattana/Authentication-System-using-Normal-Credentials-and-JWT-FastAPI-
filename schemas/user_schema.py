
from pydantic import BaseModel, EmailStr, constr
from typing_extensions import Annotated
from typing import Optional

# Request schema for signup
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: Annotated[str, constr(min_length=6)]

# Response schema (hide password)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool

    class Config:
        orm_mode = True
