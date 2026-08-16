import os
from enterprise_logger import setup_enterprise_logger

logger = setup_enterprise_logger("AeroDrift.Credentials")

def load_aws_credentials():
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    
    if not aws_access_key or not aws_secret_key:
        logger.warning("AWS Credentials not fully set in environment variables.")
    else:
        logger.info(f"Loaded AWS credentials for region {aws_region}")
        
    return {
        "region_name": aws_region,
        "aws_access_key_id": aws_access_key,
        "aws_secret_access_key": aws_secret_key
    }
