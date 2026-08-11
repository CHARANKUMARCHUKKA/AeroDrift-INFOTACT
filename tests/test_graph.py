import pytest
import networkx as nx
from graph_engine import CloudTopologyEngine

def test_engine_initialization():
    engine = CloudTopologyEngine({"ec2": [], "subnets": [], "security_groups": []})
    assert isinstance(engine.graph, nx.DiGraph)

def test_subnet_mapping():
    engine = CloudTopologyEngine({"ec2": [], "subnets": [{"subnet_id": "sub-1", "route_table_id": "rtb-1"}], "security_groups": []})
    engine.map_subnets()
    assert "sub-1" in engine.graph.nodes
    assert engine.graph.nodes["sub-1"]["type"] == "Subnet"
