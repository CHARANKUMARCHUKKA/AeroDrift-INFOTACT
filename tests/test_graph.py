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

def test_security_group_mapping():
    engine = CloudTopologyEngine({"ec2": [], "subnets": [], "security_groups": [{"group_id": "sg-1", "ingress_rules": [{"port": 80, "source": "0.0.0.0/0"}]}]})
    engine.map_security_groups()
    assert "sg-1" in engine.graph.nodes
    assert engine.graph.has_edge("0.0.0.0/0", "sg-1")

def test_ec2_mapping():
    engine = CloudTopologyEngine({"ec2": [{"instance_id": "i-1", "subnet_id": "sub-1", "security_group_ids": ["sg-1"]}], "subnets": [], "security_groups": []})
    engine.map_ec2_instances()
    assert "i-1" in engine.graph.nodes
    assert engine.graph.has_edge("sub-1", "i-1")
    assert engine.graph.has_edge("sg-1", "i-1")
