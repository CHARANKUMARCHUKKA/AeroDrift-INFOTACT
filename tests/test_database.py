import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models
import datetime

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def test_create_scan_log():
    db = TestingSessionLocal()
    log = models.SecurityScanLog(status="secure", alerts_detected="[]")
    db.add(log)
    db.commit()
    db.refresh(log)
    
    assert log.id is not None
    assert log.status == "secure"
    assert not log.remediated
    
    db.delete(log)
    db.commit()
    db.close()
