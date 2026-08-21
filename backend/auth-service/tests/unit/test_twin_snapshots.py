import pytest
from app.services.resilience_twin.twin_snapshot_engine import TwinSnapshotEngine


def test_twin_snapshots_integrity_and_history():
    engine = TwinSnapshotEngine()

    snap1 = engine.capture_snapshot("tenant_a", asset_count=50, service_count=20)
    assert snap1.snapshot_id.startswith("twn_snap_")
    assert len(snap1.integrity_hash) == 64
    assert snap1.asset_count == 50

    snap2 = engine.capture_snapshot("tenant_a", asset_count=55, service_count=22)
    assert snap2.snapshot_id != snap1.snapshot_id
    assert snap2.integrity_hash != snap1.integrity_hash

    history = engine.list_snapshots("tenant_a")
    assert len(history) == 2
    assert engine.get_latest_snapshot("tenant_a").asset_count == 55
