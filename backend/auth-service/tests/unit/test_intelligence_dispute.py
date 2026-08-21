import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_intelligence_dispute_submission():
    engine = CollaborativeDefenseEngine()
    dispute = engine.submit_dispute(
        object_id="tio_ind_ip_shadow",
        tenant_id="tenant_cloud_provider",
        reason="IP belongs to shared CDN ingress, false positive for C2.",
    )

    assert dispute.dispute_status == "OPEN"
    assert dispute.object_id == "tio_ind_ip_shadow"
    assert len(engine.list_disputes()) == 1
