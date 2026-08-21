import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_data_lineage_tracking():
    collector = GovernanceEvidenceCollector()

    ev = collector.record_evidence(
        control_id="ctrl_audit_01",
        source_system="DATA_LINEAGE_ENGINE",
        payload={"pii_flow_nodes": ["API_INGEST", "AUTH_SERVICE", "ENCRYPTED_DB"], "leakage_detected": False},
    )

    assert ev.payload["leakage_detected"] is False
