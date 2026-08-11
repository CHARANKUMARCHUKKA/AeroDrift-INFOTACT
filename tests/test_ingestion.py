import pytest
import asyncio
from aws_ingestion import fetch_ec2_instances

@pytest.mark.asyncio
async def test_ec2_fetching():
    instances = await fetch_ec2_instances()
    assert len(instances) == 2
    assert instances[0].instance_id == "i-0abcd1234efgh5678"
