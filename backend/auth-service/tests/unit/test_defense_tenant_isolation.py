import pytest
from app.services.adaptive_defense.adaptive_defense_fabric import AdaptiveDefenseFabric


def test_defense_tenant_isolation_enforced():
    fabric = AdaptiveDefenseFabric()

    fabric.posture.update_posture("tenant_alpha", threat_level="CRITICAL", active_incidents=4)
    fabric.posture.update_posture("tenant_beta", threat_level="LOW", active_incidents=0)

    pos_alpha = fabric.posture.get_or_create_posture("tenant_alpha")
    pos_beta = fabric.posture.get_or_create_posture("tenant_beta")

    assert pos_alpha.security_state == "CRITICAL"
    assert pos_beta.security_state == "NORMAL"
