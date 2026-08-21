import pytest
import time
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_intelligence_overview_performance():
    engine = GlobalThreatIntelligenceFusionEngine()
    start = time.perf_counter()
    overview = engine.get_global_intelligence_overview()
    duration_ms = (time.perf_counter() - start) * 1000.0
    assert overview is not None
    assert duration_ms < 100.0
