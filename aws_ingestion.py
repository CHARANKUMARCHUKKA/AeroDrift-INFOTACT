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
