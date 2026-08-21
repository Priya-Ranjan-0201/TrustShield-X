import pytest
from app.services.global_defense.defense_playbook_registry import DefensePlaybookRegistry

def test_global_defensive_playbook_retrieval():
    reg = DefensePlaybookRegistry()
    pbs = reg.list_playbooks()
    assert len(pbs) >= 1
    assert "T1078" in pbs[0]["target_techniques"]
