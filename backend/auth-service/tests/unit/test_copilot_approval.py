import pytest
from app.services.copilot.copilot_action_planner import CopilotActionPlanner


def test_copilot_human_approval_flow():
    planner = CopilotActionPlanner()
    plan = planner.create_plan(
        session_id="sess_appr_01",
        action_type="ISOLATE_HOST",
        target_resource="srv_checkout",
        reason="DDoS botnet node",
        evidence_ids=["ev_1"],
        expected_benefit="Drop bot traffic",
        possible_impact="Zero",
    )

    approved = planner.approve_plan(plan.plan_id, approver_id="usr_admin_dave")
    assert approved is not None
    assert approved.approval_status == "APPROVED"
