import pytest
import networkx as nx
from graph_engine import CloudTopologyEngine

def test_engine_initialization():
    engine = CloudTopologyEngine({"ec2": [], "subnets": [], "security_groups": []})
    assert isinstance(engine.graph, nx.DiGraph)
