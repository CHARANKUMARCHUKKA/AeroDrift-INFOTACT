"""
AeroDrift - Topology Graph Engine (Premium)
Uses NetworkX to model cloud architecture mathematically.
"""
import networkx as nx
import logging
from typing import Dict, Any

# Setup premium logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AeroDrift.GraphEngine")

class CloudTopologyEngine:
    """
    Encapsulates the mathematical graph logic for mapping AWS resources.
    """
    def __init__(self, cloud_state: Dict[str, Any]):
        self.cloud_state = cloud_state
        self.graph = nx.DiGraph()
        logger.info("Initialized Empty Directed Graph for Topology Mapping.")

    def map_subnets(self):
        """Maps AWS Subnets as primary nodes in the graph."""
        logger.info("Mapping Subnets into Topology...")
        for subnet in self.cloud_state.get('subnets', []):
            self.graph.add_node(
                subnet['subnet_id'], 
                type='Subnet', 
                route_table=subnet['route_table_id']
            )
    def map_security_groups(self):
        """Maps Security Groups and their ingress rules as nodes and edges."""
        logger.info("Mapping Security Groups and ingress pathways...")
        for sg in self.cloud_state.get('security_groups', []):
            self.graph.add_node(sg['group_id'], type='SecurityGroup')
            for rule in sg['ingress_rules']:
                # Traffic flows from source to the security group
                self.graph.add_edge(
                    rule['source'], 
                    sg['group_id'], 
                    port=rule['port'],
                    relation='allows_traffic'
                )
