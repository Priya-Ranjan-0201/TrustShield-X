import pytest
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry

def test_mapping_confidence_scoring():
    engine = ComplianceRequirementRegistry()
    r = engine.get_requirement("req_iso27001_a9_4_2")
    assert r.confidence in ("DIRECT", "PARTIAL", "INDIRECT", "UNCERTAIN")
