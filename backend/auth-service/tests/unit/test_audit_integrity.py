import pytest
from app.services.enterprise_governance.evidence_management_engine import EvidenceManagementEngine

def test_audit_integrity_sha256_hash():
    engine = EvidenceManagementEngine()
    ev = engine.list_evidence()[0]
    assert len(ev.integrity_hash) == 64
