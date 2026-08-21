import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_threat_hunt_hypothesis_creation():
    fabric = ThreatHuntingFabric()

    hyp = fabric.create_hunt_hypothesis(
        title="Hunt for Domain Lookalike Phishing Infrastructure",
        description="Detection of newly registered domains resembling enterprise core brand.",
        hypothesis_type="PHISHING_CAMPAIGN",
        target_assets=["corp-auth-portal.com"],
        initial_evidence=[{"source": "CertificateTransparency", "domain": "corp-auth-portall.com"}],
        tenant_id="tenant_hunt_a",
    )

    assert hyp.hypothesis_id.startswith("hpt_")
    assert hyp.status == "ACTIVE"
    assert len(hyp.alternative_hypotheses) >= 2
    assert len(hyp.supporting_evidence) == 1
