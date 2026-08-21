import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_playbook_execution():
    fabric = ThreatHuntingFabric()

    # Create hunt with NEW_DOMAIN_HUNT playbook parameters
    hyp = fabric.create_hunt_hypothesis(
        title="NEW_DOMAIN_HUNT: Lookalike domain inspection",
        description="Automated playbook testing lookalike domains",
        hypothesis_type="IMPERSONATION",
        target_assets=["secure-login-bank.com"],
    )

    res = fabric.run_bounded_hunt(hyp.hypothesis_id)
    assert res.result_id.startswith("res_")
    assert len(res.recommendations) >= 2
