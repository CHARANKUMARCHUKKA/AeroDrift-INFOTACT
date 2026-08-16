import boto3
import asyncio
from aws_credentials import load_aws_credentials
from enterprise_logger import setup_enterprise_logger
from aws_ingestion import Resource, EC2Instance, Subnet, SecurityGroup

logger = setup_enterprise_logger("AeroDrift.LiveIngestion")

class LiveAWSIngestor:
    def __init__(self):
        self.creds = load_aws_credentials()
        # Initialize boto3 clients safely
        try:
            self.ec2_client = boto3.client('ec2', **self.creds)
            logger.info("Initialized live Boto3 EC2 client successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Boto3 client: {e}")
            self.ec2_client = None

    async def fetch_all_resources(self):
        # We will populate this with actual API calls in the next commits
        return {
            "ec2": [],
            "subnets": [],
            "security_groups": []
        }
