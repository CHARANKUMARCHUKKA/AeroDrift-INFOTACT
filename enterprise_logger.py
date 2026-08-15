import logging
import json
import os
import datetime

def setup_enterprise_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
