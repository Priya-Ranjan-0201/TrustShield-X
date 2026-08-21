import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_evidence_provenance_chain():
    engine = CyberCrisisCommandEngine()
    node = engine.add_evidence_node("NODE-PROV", "t1", "C-01", "FILE", {"hash": "abc1234"}, collector="EDR-Sensor")
    assert node["collector"] == "EDR-Sensor"
    assert len(node["chain_of_custody"]) == 1
