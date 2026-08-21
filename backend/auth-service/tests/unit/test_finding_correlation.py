import pytest
from app.services.enterprise_governance.compliance_remediation_engine import ComplianceRemediationEngine

def test_finding_affected_control_correlation():
    engine = ComplianceRemediationEngine()
    f = engine.list_findings()[0]
    assert f.affected_control == "ctrl_iam_mfa_enforcement"
