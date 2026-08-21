import pytest
from app.services.enterprise_governance.evidence_management_engine import EvidenceManagementEngine

def test_evidence_access_classification():
    engine = EvidenceManagementEngine()
    ev = engine.list_evidence()[0]
    assert ev.classification == "RESTRICTED"
