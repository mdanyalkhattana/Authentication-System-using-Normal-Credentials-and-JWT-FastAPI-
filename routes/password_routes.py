from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User
from models.password_reset_model import PasswordResetToken
from schemas.password_schema import ForgotPasswordRequest
from utils.email_utils import send_reset_password_email
from utils.hashing import hash_password
from fastapi.templating import Jinja2Templates
import uuid
from utils.dependencies import get_current_user
from schemas.token_schema import TokenData

router = APIRouter(prefix="/password", tags=["Password"])
templates = Jinja2Templates(directory="templates")

# ✅ Step 1: Request password reset
@router.post("/forgot", response_model=dict)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail={"status": "error", "message": "Email not found"})

    reset_token = str(uuid.uuid4())
    token_entry = PasswordResetToken(user_id=user.id, token=reset_token)
    db.add(token_entry)
    db.commit()

    send_reset_password_email(user.email, reset_token)

    return {"status": "success", "message": "Password reset link sent to your email"}


# ✅ Step 2: Show reset password HTML form
@router.get("/reset-form", response_class=HTMLResponse)
def reset_password_form(request: Request, token: str):
    """Display HTML reset form when user clicks the email link."""
    return templates.TemplateResponse("reset_password_form.html", {"request": request, "token": token})


# ✅ Step 3: Handle password update from form
@router.post("/reset/submit", response_class=HTMLResponse)
def reset_password_submit(request: Request, token: str = Form(...), new_password: str = Form(...), db: Session = Depends(get_db)):
    """Process form and update password."""
    token_entry = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token, PasswordResetToken.is_used == False
    ).first()

    if not token_entry:
        return HTMLResponse("<h3 style='color:red;'>Invalid or expired link</h3>", status_code=400)

    user = db.query(User).filter(User.id == token_entry.user_id).first()
    if not user:
        return HTMLResponse("<h3 style='color:red;'>User not found</h3>", status_code=404)

    user.password = hash_password(new_password)
    token_entry.is_used = True
    db.commit()

    return HTMLResponse("<h3 style='color:green;'>Your password has been successfully reset.</h3>")
