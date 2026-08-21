import pytest
from app.services.global_defense.cross_tenant_correlation_guard import CrossTenantCorrelationGuard

def test_cross_tenant_correlation_disjoint_indicators():
    guard = CrossTenantCorrelationGuard()
    res = guard.correlate_signals_privacy_preserving({
        "t1": ["ioc1.com"],
        "t2": ["ioc2.com"],
    })
    assert res["shared_cross_tenant_intersections_count"] == 0
