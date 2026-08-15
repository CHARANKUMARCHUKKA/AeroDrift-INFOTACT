import os
import json
from enterprise_logger import setup_enterprise_logger

def test_json_logging():
    logger = setup_enterprise_logger("TestLogger")
    logger.info("Test message for JSON")
    
    assert os.path.exists("logs/aerodrift.json")
    
    with open("logs/aerodrift.json", "r") as f:
        lines = f.readlines()
        last_log = json.loads(lines[-1])
        
    assert last_log["level"] == "INFO"
    assert last_log["module"] == "TestLogger"
    assert last_log["message"] == "Test message for JSON"
    assert "timestamp" in last_log
