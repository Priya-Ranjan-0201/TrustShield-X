import pytest
from app.services.copilot.copilot_action_planner import CopilotActionPlanner


def test_copilot_loop_protection():
    planner = CopilotActionPlanner()

    # Plan creation is bounded and requires human approval
    plan = planner.create_plan("sess_loop", "ISOLATE", "srv_1", "reason", ["ev_1"], "benefit", "impact")
    assert plan.approval_status == "APPROVAL_REQUIRED"
