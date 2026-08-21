import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_access_certification_logging():
    collector = GovernanceEvidenceCollector()

    ev = collector.record_evidence(
        control_id="ctrl_rbac_01",
        source_system="ACCESS_CERTIFICATION_PORTAL",
        payload={"certified_by": "security_manager", "accounts_certified": 120},
    )

    assert ev.evidence_id.startswith("evi_")
    assert ev.payload["accounts_certified"] == 120
