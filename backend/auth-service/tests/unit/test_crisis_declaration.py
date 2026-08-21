import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_crisis_declaration_scope():
    engine = CyberCrisisCommandEngine()
    c = engine.declare_crisis("C-DECL", "t1", ["INC-10"], "Lead", "Ransomware Ingress", severity="SEV_1")
    assert c["severity"] == "SEV_1"
    assert "assets" in c["affected_scope"]
