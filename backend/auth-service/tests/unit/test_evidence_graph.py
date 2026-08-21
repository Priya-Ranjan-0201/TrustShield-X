import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_evidence_graph_node_addition():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-EVG", "t1", ["INC-1"], "Commander", "Test")
    node = engine.add_evidence_node("NODE-01", "t1", "C-EVG", "IP", {"ip": "198.51.100.44"})
    assert node["node_id"] == "NODE-01"
    assert node["sha256_hash"] is not None
