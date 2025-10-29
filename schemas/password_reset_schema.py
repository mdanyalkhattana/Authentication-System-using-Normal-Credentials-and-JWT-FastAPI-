from pydantic import BaseModel, EmailStr

# ✅ When user requests password reset (forgot password)
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# ✅ When user resets password using token
class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str
