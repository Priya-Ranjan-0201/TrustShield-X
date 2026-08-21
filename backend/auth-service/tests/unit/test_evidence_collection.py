import pytest
from app.services.enterprise_governance.evidence_management_engine import EvidenceManagementEngine

def test_evidence_source_provenance():
    engine = EvidenceManagementEngine()
    ev = engine.list_evidence()[0]
    assert "IAM Enclave" in ev.source
