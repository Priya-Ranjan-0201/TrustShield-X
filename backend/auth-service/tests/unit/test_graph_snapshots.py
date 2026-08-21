import pytest
from app.services.threat_intelligence_fusion.intelligence_graph_fusion_engine import IntelligenceGraphFusionEngine

def test_graph_snapshot_creation():
    engine = IntelligenceGraphFusionEngine()
    snap = engine.create_snapshot("CAMPAIGN", "cmp_darkstorm_apac")
    assert snap.snapshot_id.startswith("snap_")
    assert len(snap.snapshot_hash) == 64
