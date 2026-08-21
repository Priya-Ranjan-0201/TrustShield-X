import pytest
from app.services.fusion.security_health_engine import SecurityHealthEngine


def test_subsystem_health_and_fail_safe_degradation():
    engine = SecurityHealthEngine()

    # Normal health check
    h_normal = engine.check_subsystems_health()
    assert h_normal.overall_health == "HEALTHY"
    assert h_normal.subsystems["DATABASE_CLUSTER"].status == "HEALTHY"

    # Simulated Redis cache outage -> fail-safe reporting DEGRADED
    h_degraded = engine.check_subsystems_health(simulated_failures=["REDIS_CACHE_CLUSTER"])
    assert h_degraded.overall_health == "DEGRADED"
    assert h_degraded.subsystems["REDIS_CACHE_CLUSTER"].status == "SERVICE_DEGRADED"
    assert "fallback fail-safe" in h_degraded.subsystems["REDIS_CACHE_CLUSTER"].impact
