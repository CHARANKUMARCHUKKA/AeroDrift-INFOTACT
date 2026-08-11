import networkx as nx
import logging

logger = logging.getLogger("AeroDrift.DriftDetector")

class DriftDetector:
    def __init__(self, topology: nx.DiGraph):
        self.topology = topology
        self.alerts = []

    def scan_public_subnets(self):
        logger.info("Scanning for public subnet exposure...")
        for node, data in self.topology.nodes(data=True):
            if data.get('type') == 'Subnet' and data.get('route_table') == 'rtb-public':
                self.alerts.append(f"CRITICAL: Subnet {node} is public and exposed.")

    def scan_permissive_sgs(self):
        logger.info("Scanning for overly permissive Security Groups...")
        for u, v, data in self.topology.edges(data=True):
            if u == '0.0.0.0/0':
                self.alerts.append(f"HIGH: Security Group {v} allows public access from 0.0.0.0/0 on port {data.get('port')}.")

    def scan_ec2_exposure(self):
        logger.info("Analyzing EC2 instance blast radius...")
        for node, data in self.topology.nodes(data=True):
            if data.get('type') == 'EC2':
                pass # Placeholder for complex blast radius logic
    
    def run_all_scans(self):
        self.scan_public_subnets()
        self.scan_permissive_sgs()
        self.scan_ec2_exposure()
        return self.alerts
