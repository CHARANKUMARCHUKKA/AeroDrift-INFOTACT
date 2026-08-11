import networkx as nx
import logging

logger = logging.getLogger("AeroDrift.DriftDetector")

class DriftDetector:
    def __init__(self, topology: nx.DiGraph):
        self.topology = topology
        self.alerts = []
