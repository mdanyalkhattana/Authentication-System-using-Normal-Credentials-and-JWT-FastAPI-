from pydantic import BaseModel, EmailStr
from datetime import datetime

# ✅ Used for user registration (Sign Up)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# ✅ Used to return user info in responses
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # allows reading ORM (SQLAlchemy) objects
        
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    # def dict(self, *args, **kwargs):
    #     data = super().dict(*args, **kwargs)
    #     data.pop("password", None)  # Remove password if present
    #     return data