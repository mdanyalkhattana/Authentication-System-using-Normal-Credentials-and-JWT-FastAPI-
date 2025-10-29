from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from models.password_reset_model import PasswordReset
from schemas.password_reset_schema import ForgotPasswordRequest, ResetPasswordRequest
from utils.hashing import hash_password
from datetime import datetime, timedelta
from utils.users import get_current_user, require_role_in
import secrets

router = APIRouter(prefix="/password ",tags=[""] )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# FORGOT PASSWORD
# -------------------------
@router.post("/forgot")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db),current_user= Depends(require_role_in(["admin"]))):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = secrets.token_hex(16)
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    reset_entry = PasswordReset(
        user_id=user.id,
        reset_token=int.from_bytes(reset_token.encode(), 'little') % (10**18),
        expires_at=int(expires_at.timestamp()),
        is_used=0
    )
    db.add(reset_entry)
    db.commit()

    # Normally you'd send an email here
    return {"message": "Password reset link sent to email", "reset_token_demo": reset_token}

# -------------------------
# RESET PASSWORD
# -------------------------
@router.post("/reset")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db),current_user= Depends(require_role_in(["admin"]))):
    reset_entry = db.query(PasswordReset).filter(PasswordReset.reset_token == int.from_bytes(request.reset_token.encode(), 'little') % (10**18)).first()
    if not reset_entry or reset_entry.is_used:
        raise HTTPException(status_code=400, detail="Invalid or already used reset token")

    user = db.query(User).filter(User.id == reset_entry.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password
    user.password_hash = hash_password(request.new_password)
    reset_entry.is_used = 1
    db.commit()

    return {"message": "Password reset successful"}
