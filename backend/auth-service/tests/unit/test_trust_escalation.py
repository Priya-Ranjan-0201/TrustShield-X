import pytest
from app.services.global_defense.defense_network_manager import DefenseNetworkManager

def test_network_trust_level_explicit():
    mgr = DefenseNetworkManager()
    net = mgr.get_network("net_financial_isac")
    assert net.trust_level in ["UNTRUSTED", "OBSERVED", "VERIFIED", "TRUSTED", "RESTRICTED"]
