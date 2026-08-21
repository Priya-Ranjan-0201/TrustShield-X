import pytest
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector


def test_evidence_requirements():
    collector = GovernanceEvidenceCollector()
    ev = collector.get_evidence("evi_audit_01")

    assert ev is not None
    assert ev.freshness == "CURRENT"
    assert len(ev.integrity_hash) == 64  # SHA-256
