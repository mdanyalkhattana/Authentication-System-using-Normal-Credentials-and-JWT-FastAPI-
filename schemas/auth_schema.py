from pydantic import BaseModel, EmailStr

# ✅ Used when logging in
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ✅ Token response model
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ✅ Used for logout or checking active session (optional)
class SessionStatus(BaseModel):
    user_id: int
    is_active: bool
