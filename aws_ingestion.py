"""
AeroDrift - Cloud Ingestion Module (Premium)
Simulates high-concurrency ingestion of AWS state data.
"""
import asyncio
import json
import logging
from typing import List, Dict, Any
from dataclasses import dataclass

# Setup premium logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AeroDrift.Ingestion")

class AWSAPITimeoutError(Exception):
    """Custom exception raised when an AWS API endpoint times out."""
    pass

class AWSRateLimitError(Exception):
    """Custom exception raised when AWS API rate limits are exceeded."""
    pass

@dataclass
class EC2Instance:
    instance_id: str
    subnet_id: str
    security_group_ids: List[str]

@dataclass
class Subnet:
    subnet_id: str
    route_table_id: str

@dataclass
class SecurityGroup:
    group_id: str
    ingress_rules: List[Dict[str, Any]]

async def fetch_ec2_instances(retries=3) -> List[EC2Instance]:
    for attempt in range(retries):
        try:
            logger.info(f"Polling AWS API for EC2 instances (Attempt {attempt+1})...")
            await asyncio.sleep(1.2) # Simulate network latency
            return [
                EC2Instance(instance_id="i-0abcd1234efgh5678", subnet_id="subnet-111", security_group_ids=["sg-web"]),
                EC2Instance(instance_id="i-0wxyz9876lkjh5432", subnet_id="subnet-222", security_group_ids=["sg-db", "sg-internal"])
            ]
        except Exception as e:
            logger.warning(f"EC2 Polling failed: {str(e)}. Retrying...")
            await asyncio.sleep(2 ** attempt)
    raise AWSAPITimeoutError("Failed to fetch EC2 instances after multiple retries.")

async def fetch_subnets(retries=3) -> List[Subnet]:
    for attempt in range(retries):
        try:
            logger.info(f"Polling AWS API for Subnet routing tables (Attempt {attempt+1})...")
            await asyncio.sleep(0.8)
            return [
                Subnet(subnet_id="subnet-111", route_table_id="rtb-public"),
                Subnet(subnet_id="subnet-222", route_table_id="rtb-private")
            ]
        except Exception as e:
            logger.warning(f"Subnet Polling failed: {str(e)}. Retrying...")
            await asyncio.sleep(2 ** attempt)
    raise AWSAPITimeoutError("Failed to fetch Subnets after multiple retries.")

async def fetch_security_groups(retries=3) -> List[SecurityGroup]:
    for attempt in range(retries):
        try:
            logger.info(f"Polling AWS API for Security Group rules (Attempt {attempt+1})...")
            await asyncio.sleep(1.0)
            return [
                SecurityGroup(group_id="sg-web", ingress_rules=[{"port": 80, "source": "0.0.0.0/0"}, {"port": 443, "source": "0.0.0.0/0"}]),
                SecurityGroup(group_id="sg-db", ingress_rules=[{"port": 3306, "source": "sg-web"}]),
                SecurityGroup(group_id="sg-internal", ingress_rules=[{"port": 22, "source": "10.0.0.0/8"}])
            ]
        except Exception as e:
            logger.warning(f"Security Group Polling failed: {str(e)}. Retrying...")
            await asyncio.sleep(2 ** attempt)
    raise AWSAPITimeoutError("Failed to fetch Security Groups after multiple retries.")

async def ingest_cloud_state() -> Dict[str, Any]:
    """
    Executes all API polling concurrently using asyncio.gather for maximum performance.
    """
    logger.info("Starting highly concurrent Cloud State Ingestion with Resiliency...")
    
    # Run all I/O bound tasks concurrently
    results = await asyncio.gather(
        fetch_ec2_instances(),
        fetch_subnets(),
        fetch_security_groups(),
        return_exceptions=True
    )
    
    # Check for unhandled exceptions in gather
    for r in results:
        if isinstance(r, Exception):
            logger.error(f"Critical failure during ingestion: {str(r)}")
            raise r
            
    cloud_state = {
        "ec2": [vars(inst) for inst in results[0]],
        "subnets": [vars(sub) for sub in results[1]],
        "security_groups": [vars(sg) for sg in results[2]]
    }
    
    logger.info("Cloud State Ingestion completed successfully.")
    return cloud_state

if __name__ == "__main__":
    # Local manual testing
    logger.info("Booting AeroDrift Mock Engine...")
    state = asyncio.run(ingest_cloud_state())
    print("\n=== Ingested AWS State ===")
    print(json.dumps(state, indent=2))
