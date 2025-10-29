from sqlalchemy import Column, BigInteger, Boolean, DateTime, ForeignKey
from database import Base

class PasswordReset(Base):
    __tablename__ = "password_reset"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    reset_token = Column(BigInteger, nullable=False)
    expires_at = Column(BigInteger, nullable=False)
    is_used = Column(BigInteger, nullable=False)
