import pytest
from app.services.cyber_crisis_command.cyber_crisis_command_engine import CyberCrisisCommandEngine

def test_tenant_crisis_isolation():
    engine = CyberCrisisCommandEngine()
    engine.declare_crisis("C-T1", "tenant-1", ["INC-1"], "Lead", "Test")
    engine.declare_crisis("C-T2", "tenant-2", ["INC-2"], "Lead", "Test")
    
    list_t1 = engine.list_crises("tenant-1")
    assert len(list_t1) == 1
    assert list_t1[0]["crisis_id"] == "C-T1"
