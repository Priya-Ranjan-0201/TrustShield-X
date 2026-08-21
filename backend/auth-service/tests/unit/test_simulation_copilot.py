import pytest
from app.services.simulation.what_if_engine import WhatIfEngine


def test_copilot_simulation_grounding():
    engine = WhatIfEngine()

    res = engine.evaluate_what_if(
        target_twin_id="twn_copilot",
        question="Simulate isolating the public auth gateway",
        hypothetical_changes={"isolate_asset": "AuthGatewayAPI"},
    )

    # Invariant: Output is explicitly labeled as simulation with transparent uncertainty
    assert res.is_simulation is True
    assert res.simulated_blast_radius in ("MINIMAL", "MODERATE", "EXTENSIVE")
