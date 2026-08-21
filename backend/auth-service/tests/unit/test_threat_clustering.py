import pytest
from app.services.fusion.threat_fusion_engine import ThreatFusionEngine
from app.services.fusion.event_normalization_service import EventNormalizationService


def test_threat_clustering():
    event_service = EventNormalizationService()
    fusion_engine = ThreatFusionEngine()

    e1 = event_service.ingest_and_normalize("DETECTION", source="WEB", entity_id="phish.net", risk_score=80.0, tenant_id="tenant_clust")
    e2 = event_service.ingest_and_normalize("DETECTION", source="VOICE", entity_id="v_clone", risk_score=75.0, tenant_id="tenant_clust")

    cluster = fusion_engine.cluster_threat_events([e1, e2], cluster_type="MULTI_MODAL_ATTACK", tenant_id="tenant_clust")
    assert cluster.cluster_id.startswith("tcl_")
    assert cluster.cluster_type == "MULTI_MODAL_ATTACK"
    assert len(cluster.modalities) == 2
    assert cluster.fusion_score >= 60.0
