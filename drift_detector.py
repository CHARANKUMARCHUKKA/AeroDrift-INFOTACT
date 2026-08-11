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
