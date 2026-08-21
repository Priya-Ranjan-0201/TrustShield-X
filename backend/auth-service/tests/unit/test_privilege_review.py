import pytest
from app.services.zero_trust_exposure.privilege_governance_engine import PrivilegeGovernanceEngine

def test_privilege_review_creation():
    engine = PrivilegeGovernanceEngine()
    review = engine.create_access_review("REV-01", "t1", review_type="PERIODIC", target_scope="ALL_ADMINS")
    assert review["review_id"] == "REV-01"
    assert review["status"] == "IN_PROGRESS"
