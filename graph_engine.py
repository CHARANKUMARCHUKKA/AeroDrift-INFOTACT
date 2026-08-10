"""
AeroDrift - Topology Graph Engine (Premium)
Uses NetworkX to model cloud architecture mathematically.
"""
import networkx as nx
import logging
from typing import Dict, Any
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.tree import Tree

# Setup premium logging and Rich Console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AeroDrift.GraphEngine")

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)

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

    def map_ec2_instances(self):
        """Maps EC2 instances and connects them to their subnets and security groups."""
        logger.info("Mapping EC2 instances to Subnets and Security Groups...")
        for ec2 in self.cloud_state.get('ec2', []):
            self.graph.add_node(ec2['instance_id'], type='EC2')
            # Link to Subnet
            self.graph.add_edge(ec2['subnet_id'], ec2['instance_id'], relation='resides_in')
            # Link to Security Groups
            for sg_id in ec2['security_group_ids']:
                self.graph.add_edge(sg_id, ec2['instance_id'], relation='protected_by')

    def build(self) -> nx.DiGraph:
        """Executes the full mapping pipeline and returns the graph."""
        self.map_subnets()
        self.map_security_groups()
        self.map_ec2_instances()
        logger.info(f"Topology built successfully: {self.graph.number_of_nodes()} Nodes, {self.graph.number_of_edges()} Edges.")
        return self.graph


    def render_nodes_table(self):
        """Uses Rich to render a beautiful table of all discovered nodes."""
        table = Table(title="AeroDrift Discovered Cloud Resources", show_header=True, header_style="bold magenta")
        table.add_column("Resource ID", style="cyan", width=25)
        table.add_column("Resource Type", style="green")
        table.add_column("Metadata", style="dim")
        
        for node, data in self.graph.nodes(data=True):
            meta = ", ".join(f"{k}={v}" for k,v in data.items() if k != 'type')
            table.add_row(node, data.get('type', 'Unknown'), meta)
            
        console.print(table)

if __name__ == "__main__":
    from aws_ingestion import ingest_cloud_state
    import asyncio
    
    logger.info("Booting AeroDrift Topology Grapher...")
    # Fetch mock data
    state = asyncio.run(ingest_cloud_state())
    
    # Build Graph
    engine = CloudTopologyEngine(state)
    topology = engine.build()
    
    print("\n=== Topology Nodes ===")
    for node in topology.nodes(data=True):
        print(node)
        
    print("\n=== Topology Edges ===")
    for edge in topology.edges(data=True):
        print(edge)
