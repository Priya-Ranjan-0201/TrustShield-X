import pytest
from app.services.simulation.what_if_engine import WhatIfEngine


def test_abac_policy_change_simulation():
    engine = WhatIfEngine()

    res = engine.evaluate_what_if(
        target_twin_id="twn_policy",
        question="What if contractor access policy is expanded to core data stores?",
        hypothetical_changes={"abac_policy": "GRANT_CONTRACTOR_CORE_READ"},
    )

    assert res.simulated_risk_delta > 0.0
    assert len(res.findings) >= 1
