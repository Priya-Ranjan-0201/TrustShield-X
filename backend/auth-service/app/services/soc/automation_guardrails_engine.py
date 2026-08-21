"""
TruthShield X — Automation Guardrails & Emergency Stop Engine (Phase 21).

Enforces circuit breakers, execution depth limits, and global Emergency Pause/Resume controls.
"""

from typing import Dict, Optional
from app.schemas.autonomous_soc_models import AutomationGuardrailsDTO


class AutomationGuardrailsEngine:
    """Manages global emergency stop, depth limits, and circuit breakers."""

    def __init__(self):
        self._guardrails: Dict[str, AutomationGuardrailsDTO] = {}

    def get_guardrails(self, tenant_id: str = "default_tenant") -> AutomationGuardrailsDTO:
        if tenant_id not in self._guardrails:
            self._guardrails[tenant_id] = AutomationGuardrailsDTO(tenant_id=tenant_id)
        return self._guardrails[tenant_id]

    def pause_automation(self, tenant_id: str, user_id: str, reason: str) -> AutomationGuardrailsDTO:
        dto = AutomationGuardrailsDTO(
            tenant_id=tenant_id,
            is_paused=True,
            paused_by=user_id,
            pause_reason=reason,
            circuit_breaker_tripped=True,
        )
        self._guardrails[tenant_id] = dto
        return dto

    def resume_automation(self, tenant_id: str, user_id: str) -> AutomationGuardrailsDTO:
        dto = AutomationGuardrailsDTO(
            tenant_id=tenant_id,
            is_paused=False,
            paused_by=None,
            pause_reason=None,
            circuit_breaker_tripped=False,
        )
        self._guardrails[tenant_id] = dto
        return dto

    def is_action_permitted(self, tenant_id: str, depth: int = 1) -> bool:
        g = self.get_guardrails(tenant_id)
        if g.is_paused or g.circuit_breaker_tripped:
            return False
        if depth > g.max_execution_depth:
            return False
        return True
