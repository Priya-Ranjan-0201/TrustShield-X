import pytest
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry

def test_privacy_governance_mapping():
    engine = ComplianceRequirementRegistry()
    reqs = engine.list_requirements(framework="DPDP_2023")
    assert len(reqs) >= 1
