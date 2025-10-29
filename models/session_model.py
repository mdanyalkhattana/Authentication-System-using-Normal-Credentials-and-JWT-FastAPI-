from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from database import Base

class Session(Base):
    __tablename__ = "session"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    access_token = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
