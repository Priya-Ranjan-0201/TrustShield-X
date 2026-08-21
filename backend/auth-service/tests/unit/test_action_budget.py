import pytest
from app.services.soc.action_budget_engine import ActionBudgetEngine


def test_action_budget_exceeded_blocking():
    engine = ActionBudgetEngine()

    # Consuming beyond limit (5 assets per call)
    allowed = engine.consume_action("tenant_budget", asset_count=10)
    assert allowed is False

    budget = engine.get_budget("tenant_budget")
    assert budget.budget_exceeded is True
