import pytest
from app.services.global_defense.defense_network_manager import DefenseNetworkManager

def test_trusted_relationship_retrieval():
    mgr = DefenseNetworkManager()
    net = mgr.get_network("net_financial_isac")
    assert net is not None
    assert "tenant_finance_alpha" in net.participants
    assert net.status == "ACTIVE"
