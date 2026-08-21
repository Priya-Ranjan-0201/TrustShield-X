import pytest
from app.services.global_defense.defense_playbook_registry import DefensePlaybookRegistry

def test_security_engineering_playbook_validation():
    reg = DefensePlaybookRegistry()
    pb = reg.get_playbook("pbk_darkstorm_credential_mitigation")
    assert pb["validated_by"] == "TruthShield X Core Engineering"
