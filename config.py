import os
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.Config")

class Config:
    # Defaults to MOCK to ensure seamless local testing if AWS creds aren't set
    MODE = os.environ.get("AERODRIFT_MODE", "MOCK").upper()
    
    @classmethod
    def print_config(cls):
        logger.info(f"Initializing AeroDrift Engine in {cls.MODE} Mode.")
