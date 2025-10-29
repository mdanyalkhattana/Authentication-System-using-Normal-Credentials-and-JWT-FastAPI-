from pydantic import BaseModel, EmailStr

class EmailVerificationRequest(BaseModel):
    """
    Schema for email verification request with verification code
    """
    email: EmailStr
    verification_code: str
