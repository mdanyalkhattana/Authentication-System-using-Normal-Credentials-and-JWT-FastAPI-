from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, DateTime, func
from database import Base

class EmailVerification(Base):
    __tablename__ = "email_verification"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    email = Column(String(255), nullable=False)
    # allow longer codes (token_hex can produce 8+ chars); use 64 to be safe
    verification_code = Column(String(64), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
