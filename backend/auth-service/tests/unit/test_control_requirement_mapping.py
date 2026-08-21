import pytest
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry

def test_control_requirement_mapping_resolution():
    engine = ComplianceRequirementRegistry()
    r = engine.get_requirement("req_iso27001_a9_4_2")
    assert "ctrl_iam_mfa_enforcement" in r.mapped_controls
