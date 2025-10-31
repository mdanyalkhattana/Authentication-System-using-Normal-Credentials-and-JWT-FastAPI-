# schemas/auth_schema.py
from pydantic import BaseModel, EmailStr

# User login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# JWT Token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
