import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_resilience_tenant_isolation():
    engine = CyberResilienceEngine()
    t1 = engine.get_complete_resilience_overview("tenant_alpha")
    t2 = engine.get_complete_resilience_overview("tenant_beta")
    assert t1["tenant_id"] == "tenant_alpha"
    assert t2["tenant_id"] == "tenant_beta"
