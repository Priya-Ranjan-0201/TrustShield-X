import pytest
from app.services.global_defense.cross_tenant_correlation_guard import CrossTenantCorrelationGuard

def test_threat_signal_indicator_intersection():
    guard = CrossTenantCorrelationGuard()
    signals = {
        "tenant_a": ["c2.darkstorm.net", "198.51.100.1"],
        "tenant_b": ["c2.darkstorm.net", "203.0.113.5"],
    }
    res = guard.correlate_signals_privacy_preserving(signals)
    assert res["shared_cross_tenant_intersections_count"] == 1
    assert res["raw_tenant_data_exposed"] is False
