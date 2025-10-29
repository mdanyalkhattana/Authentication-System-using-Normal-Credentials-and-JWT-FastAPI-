from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from fastapi.responses import JSONResponse
from models.email_verification_model import EmailVerification
from schemas.email_verification_schema import EmailVerificationRequest
from datetime import datetime, timedelta
import secrets
from database import get_db
from utils.email_sender import send_verification_email
from utils.token import *

router = APIRouter(prefix="/verify", tags=["Email Verification"])

# -------------------------
# SEND VERIFICATION CODE
# -------------------------
@router.get("/verify-email")
async def send_verification(
    token: str,  # token will come in query or header
    db: Session = Depends(get_db)
):
    # ✅ Step 1: Decode token to get email
    payload = verify_access_token(token)  # this function should raise an error if expired
    email = payload.get("sub")  # assuming 'sub' stores the user email in your JWT

    if not email:
        raise HTTPException(status_code=400, detail="Invalid token or email not found")

    # ✅ Step 2: Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Step 3: Generate verification code & expiry
    code = secrets.token_hex(4)
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    user.is_verified = True
    entry = EmailVerification(
        user_id=user.id,
        email=user.email,
        verification_code=code,
        expires_at=expires_at,
        is_used=False
    )
    db.add(entry)
    db.commit()
    # ✅ Step 4: Return confirmation (email send can be handled separately)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Your Email verified successfully",
            "email": user.email,
            "expires_at": expires_at.isoformat(),            
        },
        status_code=status.HTTP_200_OK
    )


# -------------------------
# VERIFY EMAIL
# -------------------------
# @router.post("/confirm")
# def confirm_verification(request: EmailVerificationRequest, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     record = db.query(EmailVerification).filter(
#         EmailVerification.user_id == user.id,
#         EmailVerification.verification_code == request.verification_code,
#         EmailVerification.is_used == False
#     ).first()

#     if not record:
#         raise HTTPException(status_code=400, detail="Invalid or expired code")

#     user.is_verified = True
#     record.is_used = True
#     db.commit()

#     return {"message": "Email verified successfully"}
