import pytest
from app.services.resilience_twin.simulation_reality_comparator import SimulationRealityComparator


def test_simulation_reality_match_and_divergence():
    comparator = SimulationRealityComparator()

    # Small delta -> MATCH
    match_res = comparator.compare_outcome("sim_01", expected_residual_risk=15.0, actual_residual_risk=16.0)
    assert match_res.classification == "MATCH"
    assert match_res.error_delta == 1.0

    # Large delta -> DIVERGENCE
    div_res = comparator.compare_outcome("sim_02", expected_residual_risk=10.0, actual_residual_risk=32.0)
    assert div_res.classification == "DIVERGENCE"
    assert div_res.root_cause is not None
