import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric


def test_hunt_evidence_collection():
    fabric = ThreatHuntingFabric()

    fabric.query.populate_test_telemetry("tenant_ev", [
        {"asset": "api.gateway", "exposure_score": 65.0, "source": "ExposureEngine"},
    ])

    hyp = fabric.create_hunt_hypothesis("Investigate API Gateway Exposure", "Scan", "EXPOSURE_ESCALATION", tenant_id="tenant_ev")
    res = fabric.run_bounded_hunt(hyp.hypothesis_id)

    assert res.result_id is not None
    assert len(res.limitations) >= 1
