import pytest
from app.services.collective_defense.intelligence_dispute_engine import IntelligenceDisputeEngine


def test_dispute_submission_and_resolution():
    engine = IntelligenceDisputeEngine()

    dispute = engine.submit_dispute(
        intelligence_id="tio_test_123",
        tenant_id="tenant_delta",
        dispute_type="FALSE_POSITIVE",
        reason="Subdomain is our internal load balancer",
        evidence="Internal DNS registration records provided",
    )

    assert dispute.status == "OPEN"
    assert dispute.dispute_id.startswith("dsp_")

    resolved = engine.resolve_dispute(
        dispute.dispute_id,
        resolution="Approved dispute, downgraded to benign",
        status="RESOLVED",
        reviewer_notes="Verified against tenant public PKI infrastructure",
    )

    assert resolved is not None
    assert resolved.status == "RESOLVED"
    assert resolved.resolved_at is not None
