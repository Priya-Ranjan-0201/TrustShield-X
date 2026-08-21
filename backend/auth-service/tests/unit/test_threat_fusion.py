import pytest
from app.services.fusion.threat_fusion_engine import ThreatFusionEngine
from app.services.fusion.event_normalization_service import EventNormalizationService


def test_multi_modal_threat_fusion_score():
    event_service = EventNormalizationService()
    fusion_engine = ThreatFusionEngine()

    e_web = event_service.ingest_and_normalize("DETECTION", source="WEB", risk_score=80.0, tenant_id="tenant_fuse")
    e_apk = event_service.ingest_and_normalize("DETECTION", source="APK", risk_score=85.0, tenant_id="tenant_fuse")
    e_upi = event_service.ingest_and_normalize("DETECTION", source="UPI", risk_score=90.0, tenant_id="tenant_fuse")

    score_dto = fusion_engine.calculate_fusion_score([e_web, e_apk, e_upi])
    assert score_dto.fusion_score >= 75.0
    assert len(score_dto.converged_modalities) == 3
    assert "Cross-modal convergence" in score_dto.explanation
    assert score_dto.confidence >= 0.90
