import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_access_reviews_evidence():
    collector = GovernanceEvidenceCollector()

    ev = collector.record_evidence(
        control_id="ctrl_rbac_01",
        source_system="ACCESS_REVIEW_ENGINE",
        payload={"dormant_accounts_found": 0, "excessive_privileges_revoked": 2},
    )

    assert ev.source_system == "ACCESS_REVIEW_ENGINE"
    assert ev.freshness == "CURRENT"
