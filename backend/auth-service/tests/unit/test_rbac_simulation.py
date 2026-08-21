import pytest
from app.services.simulation.what_if_engine import WhatIfEngine


def test_rbac_privilege_escalation_simulation():
    engine = WhatIfEngine()

    res = engine.evaluate_what_if(
        target_twin_id="twn_rbac",
        question="What if SecurityAnalyst role is granted admin export permissions?",
        hypothetical_changes={"rbac_grant": "admin.export"},
    )

    assert res.simulated_risk_delta >= 10.0
    assert res.is_simulation is True
