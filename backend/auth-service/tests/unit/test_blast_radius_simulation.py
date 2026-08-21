import pytest
from app.services.simulation.what_if_engine import WhatIfEngine


def test_blast_radius_simulation():
    engine = WhatIfEngine()

    res = engine.evaluate_what_if(
        target_twin_id="twn_blast",
        question="What if API Gateway certificate expires unexpectedly?",
        hypothetical_changes={"cert_expiry": True},
    )

    assert res.simulated_blast_radius in ("MINIMAL", "MODERATE", "EXTENSIVE")
    assert len(res.affected_assets) >= 1
