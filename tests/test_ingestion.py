import pytest
import asyncio
from aws_ingestion import fetch_ec2_instances

@pytest.mark.asyncio
async def test_ec2_fetching():
    instances = await fetch_ec2_instances()
    assert len(instances) == 2
    assert instances[0].instance_id == "i-0abcd1234efgh5678"

from aws_ingestion import fetch_subnets
@pytest.mark.asyncio
async def test_subnet_fetching():
    subnets = await fetch_subnets()
    assert len(subnets) == 2
    assert subnets[0].subnet_id == "subnet-111"

from aws_ingestion import AWSAPITimeoutError
@pytest.mark.asyncio
async def test_api_timeout():
    with pytest.raises(AWSAPITimeoutError):
        # Placeholder for advanced mock test
        pass 
