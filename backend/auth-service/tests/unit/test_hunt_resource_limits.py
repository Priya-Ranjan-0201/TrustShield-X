import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric
from app.schemas.hunting_models import HuntBudgetConfigDTO


def test_hunt_bounded_resource_limits():
    fabric = ThreatHuntingFabric()

    # Populate 500 records
    large_telemetry = [{"asset": f"host_{i}.corp", "exposure_score": 60.0} for i in range(500)]
    fabric.query.populate_test_telemetry("tenant_budget", large_telemetry)

    hyp = fabric.create_hunt_hypothesis("Bounded Hunt Test", "Testing budget", "UNKNOWN_THREAT", tenant_id="tenant_budget")

    # Limit budget to 25 records
    budget = HuntBudgetConfigDTO(max_records_to_scan=25, max_duration_seconds=5)
    res = fabric.run_bounded_hunt(hyp.hypothesis_id, budget=budget)

    assert res.result_id is not None
    assert len(res.limitations) >= 1
