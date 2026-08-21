import pytest
from app.services.copilot.copilot_action_planner import CopilotActionPlanner


def test_copilot_action_plan_creation():
    planner = CopilotActionPlanner()
    plan = planner.create_plan(
        session_id="sess_plan_01",
        action_type="QUARANTINE_SERVICE",
        target_resource="srv_payment_gateway",
        reason="Active RCE vulnerability exploited",
        evidence_ids=["ev_pcap_trace_88"],
        expected_benefit="Prevent lateral spread",
        possible_impact="Disrupt webhook listener",
    )

    assert plan.plan_id.startswith("act_plan_")
    assert plan.approval_status == "APPROVAL_REQUIRED"
    assert plan.required_approval_tier == "TIER_2_FOUR_EYES"
