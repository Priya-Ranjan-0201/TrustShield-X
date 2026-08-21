import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_governance_evidence_recording():
    collector = GovernanceEvidenceCollector()

    ev = collector.record_evidence(
        control_id="ctrl_dr_01",
        source_system="DR_SIMULATION_ENGINE",
        payload={"failover_duration_seconds": 4.5, "data_loss_bytes": 0},
    )

    assert ev.evidence_id.startswith("evi_")
    assert ev.freshness == "CURRENT"
    assert ev.source_system == "DR_SIMULATION_ENGINE"
