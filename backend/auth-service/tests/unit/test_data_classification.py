import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_evidence_classification():
    engine = CyberCrisisCommandEngine()
    node = engine.add_evidence_node("N-CLASS", "t1", "C-1", "DB", {"table": "users"}, classification="RESTRICTED")
    assert node["classification"] == "RESTRICTED"
