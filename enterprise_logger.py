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
    return logger
