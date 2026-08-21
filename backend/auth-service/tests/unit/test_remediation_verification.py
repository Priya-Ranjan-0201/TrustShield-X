import pytest
from app.services.assurance_fabric.remediation_engine import RemediationEngine

def test_remediation_verification():
    engine = RemediationEngine()
    plan = engine.create_remediation_plan("ctl_1", "Config drift", ["Fix config"])
    reval = engine.revalidate_remediation(plan.remediation_id, test_passed=True)
    assert reval.execution_status == "REMEDIATED"
    failed_reval = engine.revalidate_remediation(plan.remediation_id, test_passed=False)
    assert failed_reval.execution_status == "REMEDIATION_NOT_VERIFIED"
