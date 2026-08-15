import logging
import json
import os
import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage()
        }
        return json.dumps(log_obj)

def setup_enterprise_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if logger.handlers:
        return logger
        
    os.makedirs("logs", exist_ok=True)
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler("logs/aerodrift.json", maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(JSONFormatter())
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False 
    
    return logger
