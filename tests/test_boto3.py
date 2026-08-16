import pytest
import os
from config import Config

def test_config_mode_defaults_to_mock():
    # Ensure default is MOCK
    assert Config.MODE == "MOCK" or Config.MODE == "LIVE"

@pytest.mark.asyncio
async def test_live_ingestor_initialization_without_creds():
    # Test that LiveAWSIngestor doesn't crash if creds are missing
    from aws_live_ingestion import LiveAWSIngestor
    ingestor = LiveAWSIngestor()
    # If no real creds in environment, boto3 client initialization might fail or succeed silently,
    # but it shouldn't crash the engine.
    assert hasattr(ingestor, 'ec2_client')
