import pytest
from app.services.enterprise_governance.access_review_governance_engine import AccessReviewGovernanceEngine

def test_access_review_certification():
    engine = AccessReviewGovernanceEngine()
    res = engine.perform_privileged_access_review("default_tenant")
    assert res["status"] == "ACCESS_REVIEW_CERTIFIED"
    assert res["orphan_accounts_detected"] == 0
