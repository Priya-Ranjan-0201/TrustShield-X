import pytest
from app.services.resilience.resilience_gap_engine import ResilienceGapEngine

def test_resilience_gaps():
    engine = ResilienceGapEngine()
    gaps = engine.detect_gaps(backup_age_hours=36.0, failover_tested=False)
    assert len(gaps) >= 2
    types = [g.gap_type for g in gaps]
    assert "STALE_BACKUP" in types
    assert "UNTESTED_BACKUP" in types
