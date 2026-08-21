import pytest
from app.services.enterprise_governance.access_review_governance_engine import AccessReviewGovernanceEngine

def test_privileged_identities_count():
    engine = AccessReviewGovernanceEngine()
    res = engine.perform_privileged_access_review("default_tenant")
    assert res["total_privileged_identities"] >= 1
