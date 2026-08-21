import pytest
from app.services.federation.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine


def test_restricted_classification_blocks_global_sharing():
    engine = IntelligenceSharingPolicyEngine()

    decision = engine.evaluate_sharing(
        payload_data={"threat": "targeted_apt_sample"},
        requested_scope="GLOBAL",
        data_classification="RESTRICTED",
    )
    assert decision.decision == "SHARE_INTERNAL_ONLY"
    assert "exceeds GLOBAL sharing clearance" in decision.reason
