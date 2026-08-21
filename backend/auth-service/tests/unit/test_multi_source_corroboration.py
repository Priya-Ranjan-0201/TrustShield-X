import pytest
from app.services.threat_intelligence_fusion.multi_source_corroboration_engine import MultiSourceCorroborationEngine

def test_multi_source_independent_corroboration():
    engine = MultiSourceCorroborationEngine()
    claims = [
        {"source_id": "src_cert_in", "content": "Advisory text from CERT-In"},
        {"source_id": "src_fs_isac", "content": "Banking advisory from FS-ISAC"},
        {"source_id": "src_vendor", "content": "Threat report from Vendor"},
    ]
    res = engine.calculate_corroboration(claims)
    assert res["effective_independent_sources"] == 3
    assert res["is_syndicated_reproduction"] is False
    assert res["corroboration_confidence"] >= 0.90
