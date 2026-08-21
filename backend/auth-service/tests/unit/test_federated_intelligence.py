import pytest
from app.services.global_defense.cross_tenant_correlation_guard import CrossTenantCorrelationGuard

def test_federated_zero_knowledge_aggregation():
    guard = CrossTenantCorrelationGuard()
    res = guard.correlate_signals_privacy_preserving({
        "t1": ["bad_domain.com"],
        "t2": ["bad_domain.com"],
        "t3": ["bad_domain.com"],
    })
    assert res["privacy_guard_enforced"] is True
    assert res["intersections"][0]["participating_tenant_count"] == 3
