import pytest
from app.services.global_defense.defense_network_manager import DefenseNetworkManager

def test_participant_membership():
    mgr = DefenseNetworkManager()
    net = mgr.get_network("net_financial_isac")
    assert "tenant_finance_alpha" in net.participants
    assert "tenant_cloud_beta" in net.participants
