from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from database import Base
from datetime import datetime

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    action = Column(String(255), nullable=False)
    ip_address = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
