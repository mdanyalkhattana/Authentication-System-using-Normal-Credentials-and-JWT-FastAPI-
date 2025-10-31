from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User
from models.email_verification_model import EmailVerificationToken
from datetime import datetime, timedelta

router = APIRouter(prefix="/verify", tags=["Email Verification"])

@router.get("/email")
def verify_email(token: str, db: Session = Depends(get_db)):
    # Find token
    db_token = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token,
        EmailVerificationToken.is_used == False
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )

    # Find user
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mark user as verified
    user.is_verified = True
    db_token.is_used = True
    db.commit()

    return {"message": "Email verified successfully! You can now log in."}
