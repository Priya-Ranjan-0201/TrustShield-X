import pytest
from app.services.assurance_fabric.remediation_engine import RemediationEngine

def test_assurance_rbac():
    engine = RemediationEngine()
    plan = engine.create_remediation_plan("ctl_1", "Policy drift", ["Fix policy"])
    approved = engine.approve_and_execute(plan.remediation_id, approver_id="usr_ciso")
    assert approved.approver_id == "usr_ciso"
