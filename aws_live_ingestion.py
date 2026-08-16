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
        
    async def fetch_ec2_instances(self):
        if not self.ec2_client: return []
        logger.info("Polling real AWS API for EC2 instances...")
        try:
            # We use a thread pool to avoid blocking the asyncio event loop with boto3 sync calls
            response = await asyncio.to_thread(self.ec2_client.describe_instances)
            instances = []
            for res in response.get('Reservations', []):
                for inst in res.get('Instances', []):
                    instances.append(EC2Instance(id=inst['InstanceId'], type="EC2", subnet_id=inst.get('SubnetId', '')))
            return instances
        except Exception as e:
            logger.error(f"Error fetching EC2 instances: {e}")
            return []

    async def fetch_all_resources(self):
        ec2_instances = await self.fetch_ec2_instances()
        return {
            "ec2": ec2_instances,
            "subnets": [],
            "security_groups": []
        }
