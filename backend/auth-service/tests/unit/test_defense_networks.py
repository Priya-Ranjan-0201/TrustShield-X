import pytest
from app.services.global_defense.defense_network_manager import DefenseNetworkManager

def test_defense_network_lifecycle():
    mgr = DefenseNetworkManager()
    net = mgr.create_network("Healthcare ISAC", ["tenant_med_1", "tenant_med_2"], trust_level="VERIFIED", duration_days=30)
    assert net.name == "Healthcare ISAC"
    assert net.trust_level == "VERIFIED"
    assert net.status == "ACTIVE"
    assert len(mgr.list_networks()) >= 2
