import pytest
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_intelligence_concurrency_resilience():
    engine = GlobalThreatIntelligenceFusionEngine()
    for i in range(10):
        rec = engine.ingest_record("src_global_exchange", {"indicator": f"ioc-{i}.test.net", "confidence": 0.90})
        assert rec.indicator == f"ioc-{i}.test.net"
