import pytest
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry

def test_data_retention_dpdp_safeguards():
    engine = ComplianceRequirementRegistry()
    r = engine.get_requirement("req_dpdp_sec_8_5")
    assert r is not None
    assert r.framework == "DPDP_2023"
