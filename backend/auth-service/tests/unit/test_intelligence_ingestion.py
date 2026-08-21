import pytest
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_intelligence_ingestion_pipeline():
    engine = GlobalThreatIntelligenceFusionEngine()
    record = engine.ingest_record("src_global_exchange", {"indicator": "c2.attacker.com", "severity": "HIGH", "confidence": 0.95})
    assert record.indicator == "c2.attacker.com"
    assert record.claim_status == "REPORTED"
    assert len(engine.list_records()) >= 1
