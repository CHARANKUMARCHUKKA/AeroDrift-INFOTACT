from sqlalchemy import Column, Integer, String, Boolean, DateTime
import datetime
from database import Base

class SecurityScanLog(Base):
    __tablename__ = "security_scans"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, index=True)
    alerts_detected = Column(String)
    remediated = Column(Boolean, default=False)
