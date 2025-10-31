# routes/session_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.session_model import Session as UserSession
from models.user_model import User
from utils.dependencies import get_current_user
from schemas.token_schema import TokenData

router = APIRouter(prefix="/session", tags=["Session"])

@router.post("/logout", response_model=dict)
def logout_user( db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    """
    Logout API without token input.
    - Takes user_id (from frontend or current session)
    - Deactivates the user's active session
    - Returns clean JSON message
    """

    # Step 1: Find active session for the user
    session = db.query(UserSession).filter(
        # UserSession.user_id == user_id,
        UserSession.is_active == True
    ).first()

    # Step 2: If no active session found
    if not session:
        return {
            "status": "info",
            "message": "User already logged out or no active session"
        }

    # Step 3: Mark session as inactive
    session.is_active = False
    db.commit()

    # Step 4: Return success response
    return {
        "status": "success",
        "message": "User logged out successfully"
    }
