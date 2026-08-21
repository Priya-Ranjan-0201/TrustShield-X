import pytest
from app.services.adaptive_defense.environment_discovery_engine import EnvironmentDiscoveryEngine


def test_environment_snapshot_capture_and_versioning():
    engine = EnvironmentDiscoveryEngine()

    snap1 = engine.capture_snapshot("tenant_1", assets=["srv-01", "srv-02"], services=["auth", "billing"])
    assert snap1.version == 1
    assert len(snap1.assets) == 2

    snap2 = engine.capture_snapshot("tenant_1", assets=["srv-01", "srv-02", "srv-03"], services=["auth", "billing"])
    assert snap2.version == 2
    assert len(snap2.assets) == 3

    latest = engine.get_latest_snapshot("tenant_1")
    assert latest.version == 2
