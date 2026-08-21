import pytest
from app.services.global_defense.coordination_timeline_engine import CoordinationTimelineEngine

def test_coordination_timeline_milestone_recording():
    engine = CoordinationTimelineEngine()
    m = engine.record_milestone("coord_01", "APPROVED", "CISO and SOC Lead approved response plan")
    assert m["milestone"] == "APPROVED"
    timeline = engine.get_timeline("coord_01")
    assert len(timeline) >= 1
