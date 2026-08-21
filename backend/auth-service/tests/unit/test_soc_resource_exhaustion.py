import pytest
from app.services.soc.action_budget_engine import ActionBudgetEngine


def test_soc_resource_exhaustion_rate_limiting():
    engine = ActionBudgetEngine()

    # Exhaust budget of 50 actions per hour
    for i in range(50):
        assert engine.consume_action("tenant_burst", asset_count=1) is True

    # 51st action must be blocked
    assert engine.consume_action("tenant_burst", asset_count=1) is False
