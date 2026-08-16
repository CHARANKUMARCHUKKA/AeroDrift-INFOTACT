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
        
            
    async def fetch_subnets(self):
        if not self.ec2_client: return []
        logger.info("Polling real AWS API for Subnets...")
        try:
            response = await asyncio.to_thread(self.ec2_client.describe_subnets)
            subnets = []
            for sub in response.get('Subnets', []):
                is_public = sub.get('MapPublicIpOnLaunch', False)
                route_table = "rtb-public" if is_public else "rtb-private"
                subnets.append(Subnet(id=sub['SubnetId'], type="Subnet", route_table=route_table))
            return subnets
        except Exception as e:
            logger.error(f"Error fetching Subnets: {e}")
            return []

    async def fetch_all_resources(self):
        
            
    async def fetch_security_groups(self):
        if not self.ec2_client: return []
        logger.info("Polling real AWS API for Security Groups...")
        try:
            response = await asyncio.to_thread(self.ec2_client.describe_security_groups)
            sgs = []
            for sg in response.get('SecurityGroups', []):
                rules = []
                for perm in sg.get('IpPermissions', []):
                    port = perm.get('FromPort', 'all')
                    for ip_range in perm.get('IpRanges', []):
                        rules.append({"port": port, "source": ip_range.get('CidrIp')})
                sgs.append(SecurityGroup(id=sg['GroupId'], type="SecurityGroup", ingress_rules=rules))
            return sgs
        except Exception as e:
            logger.error(f"Error fetching Security Groups: {e}")
            return []

    async def fetch_all_resources(self):
        ec2_instances, subnets, sgs = await asyncio.gather(
            self.fetch_ec2_instances(),
            self.fetch_subnets(),
            self.fetch_security_groups()
        )
        return {
            "ec2": ec2_instances,
            "subnets": subnets,
            "security_groups": sgs
        }
        }
