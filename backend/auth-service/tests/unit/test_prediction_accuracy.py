import pytest
from app.services.resilience_twin.simulation_reality_comparator import SimulationRealityComparator


def test_prediction_accuracy_statistical_metrics():
    comparator = SimulationRealityComparator()
    metrics = comparator.get_accuracy_metrics()

    assert metrics.precision > 0.85
    assert metrics.recall > 0.85
    assert metrics.calibration > 0.90
    assert metrics.status == "STATISTICALLY_SUPPORTED"
