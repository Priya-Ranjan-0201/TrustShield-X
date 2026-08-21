import pytest
from app.services.enterprise_governance.compliance_remediation_engine import ComplianceRemediationEngine

def test_finding_management_listing():
    engine = ComplianceRemediationEngine()
    findings = engine.list_findings()
    assert len(findings) >= 1
    assert findings[0].severity == "HIGH"
