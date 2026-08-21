import pytest
from app.services.resilience_twin.simulation_reality_comparator import SimulationRealityComparator


def test_model_calibration_updates():
    comparator = SimulationRealityComparator()

    init_samples = comparator._sample_count
    comparator.compare_outcome("sim_cal_01", expected_residual_risk=20.0, actual_residual_risk=23.5)

    assert comparator._sample_count == init_samples + 1
    assert len(comparator._calibration_records) >= 1
    assert comparator._calibration_records[-1].average_error_pct > 0.0
