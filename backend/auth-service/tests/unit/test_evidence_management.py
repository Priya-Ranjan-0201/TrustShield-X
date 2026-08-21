import pytest
from app.services.enterprise_governance.evidence_management_engine import EvidenceManagementEngine

def test_evidence_management_listing():
    engine = EvidenceManagementEngine()
    evs = engine.list_evidence()
    assert len(evs) >= 1
    assert evs[0].classification == "RESTRICTED"
