import pytest
from app.services.global_defense.defense_playbook_registry import DefensePlaybookRegistry

def test_playbook_safety_rollback_present():
    reg = DefensePlaybookRegistry()
    pb = reg.get_playbook("pbk_darkstorm_credential_mitigation")
    assert "rollback_procedure" in pb
    assert len(pb["rollback_procedure"]) > 0
