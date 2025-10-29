from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User
from fastapi.responses import JSONResponse
from models.session_model import Session as UserSession
from models.email_verification_model import EmailVerification
from schemas.user_schema import UserCreate, UserResponse
from schemas.auth_schema import LoginRequest, TokenResponse
from utils.hashing import hash_password, verify_password
from utils.token import create_access_token
from utils.email_sender import send_verification_email
from datetime import datetime, timedelta
import secrets
from database import get_db
from utils.users import get_current_user,require_role_in

router = APIRouter(prefix="/auth", tags=[" Authentication"])

# --------------------------
# SIGN UP (Register New User)
# --------------------------
@router.post("/signup", response_model=UserResponse)
async def signup(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=request.username,
        email=request.email,
        password_hash=hash_password(request.password),
        is_verified=False,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate verification code and send email
    code = secrets.token_hex(4)
    expires_at = datetime.utcnow() + timedelta(minutes=10)

    verification_entry = EmailVerification(
        user_id=new_user.id,
        email=new_user.email,
        verification_code=code,
        expires_at=expires_at
    )
    db.add(verification_entry)
    db.commit()


    # Send verification email
    try:
        sent = await send_verification_email(new_user.email)
        message = "User created successfully and verification email sent" if sent else "User created successfully (email sending failed)"
    except Exception as e:
        print(f"[auth_routes] email send error: {e}")
        message = "User created successfully (email sending failed)"

    user_response = UserResponse.model_validate(new_user)
    # model_dump(mode="json") returns JSON-serializable types (dates -> ISO strings)
    return JSONResponse(
        content={
            "status": status.HTTP_201_CREATED,
            "message": message,
            "data": user_response.model_dump(mode="json"),            
        },
        status_code=status.HTTP_201_CREATED
    )

# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(
          request: LoginRequest,
        #   email: str = Form(None),
        #   password: str = Form(None),          
          db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    # Check for active session
    active_session = db.query(UserSession).filter(UserSession.user_id == user.id, UserSession.is_active == True).first()
    if active_session:
        raise HTTPException(status_code=400, detail="Session already active")

    # Create access token
    access_token = create_access_token(data={"sub": user.email})

    # Save session
    new_session = UserSession(
        user_id=user.id,
        access_token=access_token,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        is_active=True
    )
    db.add(new_session)
    db.commit()
    user_response = UserResponse.model_validate(user)
    # return {"access_token": access_token, "token_type": "bearer"}
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": " Login successful",
            "data": user_response.model_dump(mode="json"),   
            "access_token": access_token, "token_type": "bearer"         
        },
        status_code=status.HTTP_200_OK
    )

# -------------------------
# LOGOUT    ,current_user: User = Depends(get_current_user
# -------------------------
@router.post("/logout")
def logout(user_id: int, db: Session = Depends(get_db),current_user= Depends(require_role_in(["admin"]))):
    session = db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.is_active == True).first()
    if not session:
        raise HTTPException(status_code=404, detail="No active session found")

    session.is_active = False
    db.commit()
    return {"message": "Logged out successfully"}
