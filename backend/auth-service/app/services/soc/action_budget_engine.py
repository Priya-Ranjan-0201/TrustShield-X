"""
TruthShield X — Action Budget Engine (Phase 21).

Enforces operational action budgets to prevent cascading automated changes.
"""

from typing import Dict
from app.schemas.autonomous_soc_models import ResponseActionBudgetDTO


class ActionBudgetEngine:
    """Tracks and enforces limits on actions per hour, blast radius, and affected assets."""

    def __init__(self):
        self._budgets: Dict[str, ResponseActionBudgetDTO] = {}

    def get_budget(self, tenant_id: str = "default_tenant") -> ResponseActionBudgetDTO:
        if tenant_id not in self._budgets:
            self._budgets[tenant_id] = ResponseActionBudgetDTO(tenant_id=tenant_id)
        return self._budgets[tenant_id]

    def consume_action(self, tenant_id: str = "default_tenant", asset_count: int = 1) -> bool:
        budget = self.get_budget(tenant_id)
        if budget.current_action_count + 1 > budget.max_actions_per_hour or asset_count > budget.max_affected_assets:
            self._budgets[tenant_id] = ResponseActionBudgetDTO(
                tenant_id=tenant_id,
                max_actions_per_hour=budget.max_actions_per_hour,
                current_action_count=budget.current_action_count,
                max_blast_radius_pct=budget.max_blast_radius_pct,
                max_affected_assets=budget.max_affected_assets,
                budget_exceeded=True,
            )
            return False

        self._budgets[tenant_id] = ResponseActionBudgetDTO(
            tenant_id=tenant_id,
            max_actions_per_hour=budget.max_actions_per_hour,
            current_action_count=budget.current_action_count + 1,
            max_blast_radius_pct=budget.max_blast_radius_pct,
            max_affected_assets=budget.max_affected_assets,
            budget_exceeded=False,
        )
        return True
