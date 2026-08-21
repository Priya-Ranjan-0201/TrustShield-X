import pytest
from app.services.enterprise_governance.compliance_requirement_registry import ComplianceRequirementRegistry

def test_requirement_registry_frameworks():
    engine = ComplianceRequirementRegistry()
    reqs = engine.list_requirements()
    assert len(reqs) >= 2
    frameworks = [r.framework for r in reqs]
    assert "ISO_27001" in frameworks
    assert "DPDP_2023" in frameworks
