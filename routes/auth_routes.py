from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse
from utils.hashing import hash_password
from utils.email_utils import send_verification_email
from database import get_db
import uuid
from models.email_verification_model import EmailVerificationToken
from models.session_model import Session as UserSession
from schemas.auth_schema import LoginRequest, TokenResponse
from utils.hashing import verify_password
from utils.jwt_utils import create_access_token
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_pw = hash_password(user.password)

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token
    verify_token = str(uuid.uuid4())
    token_entry = EmailVerificationToken(
        user_id=new_user.id,
        token=verify_token
    )
    db.add(token_entry)
    db.commit()

    # Send email
    send_verification_email(new_user.email, verify_token)

    # return new_user
    return JSONResponse(
        content={
            "status": status.HTTP_201_CREATED,
            "message": "User registered successfully. Please check your email for verification.", 
             
        },
        status_code=status.HTTP_201_CREATED
    )


# router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=dict)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    """
    1️⃣ Check if user exists.
    2️⃣ Verify user is verified.
    3️⃣ Check if already logged in (active session).
    4️⃣ Validate password using Argon2.
    5️⃣ Create JWT access token.
    6️⃣ Save new session in DB.
    7️⃣ Return JSON response.
    """

    # Step 1: Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "Invalid email or password"}
        )

    # Step 2: Check if verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "User not verified yet"}
        )

    # Step 3: Check active session
    existing_session = db.query(UserSession).filter(
        UserSession.user_id == user.id, UserSession.is_active == True
    ).first()
    if existing_session:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "error", "message": "Session already exists"}
        )

    # Step 4: Verify password
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "Invalid email or password"}
        )

    # Step 5: Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Step 6: Store session
    new_session = UserSession(user_id=user.id, token=access_token, is_active=True)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Step 7: Return JSON success response
    return {
        "status": "success",
        "message": "Login successful",
        "data": {
            "user_id": user.id,
            "email": user.email,
            "access_token": access_token
        }
    }