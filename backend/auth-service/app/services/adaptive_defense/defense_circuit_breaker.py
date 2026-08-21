"""
TruthShield X — Defense Circuit Breaker & Emergency Kill Switch (Phase 17).

Provides runaway loop protection, failure trip thresholds, and global emergency kill switch.
"""

from typing import Dict, Optional, Set
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import (
    DefenseCircuitBreakerDTO,
    AutomationControlStateDTO,
    CircuitBreakerStateLiteral,
)


class DefenseCircuitBreaker:
    """Automated defense circuit breaker and emergency kill switch controller."""

    def __init__(self):
        # tenant_id -> DefenseCircuitBreakerDTO
        self._breakers: Dict[str, DefenseCircuitBreakerDTO] = {}
        # tenant_id -> AutomationControlStateDTO
        self._control_states: Dict[str, AutomationControlStateDTO] = {}
        self._executed_actions_window: Set[str] = set()

    def get_or_create_breaker(self, tenant_id: str = "default_tenant") -> DefenseCircuitBreakerDTO:
        if tenant_id not in self._breakers:
            self._breakers[tenant_id] = DefenseCircuitBreakerDTO(tenant_id=tenant_id)
        return self._breakers[tenant_id]

    def get_or_create_control_state(self, tenant_id: str = "default_tenant") -> AutomationControlStateDTO:
        if tenant_id not in self._control_states:
            self._control_states[tenant_id] = AutomationControlStateDTO(tenant_id=tenant_id)
        return self._control_states[tenant_id]

    def can_execute_automated_action(self, tenant_id: str, action_key: str) -> bool:
        """Evaluates whether automation is allowed to proceed."""
        breaker = self.get_or_create_breaker(tenant_id)
        control = self.get_or_create_control_state(tenant_id)

        # 1. Check Global Emergency Kill Switch (Section 49)
        if breaker.kill_switch_active or control.kill_switch_active or not control.automation_enabled:
            return False

        # 2. Check Circuit Breaker State (Section 48)
        if breaker.state == "OPEN":
            return False

        # 3. Action Loop Deduplication (Section 47)
        if action_key in self._executed_actions_window:
            return False

        return True

    def record_action_execution(self, action_key: str):
        self._executed_actions_window.add(action_key)

    def record_failure(self, tenant_id: str, reason: str):
        """Records an execution failure and trips circuit breaker if threshold is exceeded."""
        breaker = self.get_or_create_breaker(tenant_id)
        breaker.consecutive_failures += 1

        if breaker.consecutive_failures >= breaker.failure_threshold:
            breaker.state = "OPEN"
            breaker.last_tripped_at = datetime.now(timezone.utc).isoformat()
            breaker.trip_reason = f"Consecutive failure threshold exceeded: {reason}"

            control = self.get_or_create_control_state(tenant_id)
            control.circuit_breaker_state = "OPEN"

    def record_success(self, tenant_id: str):
        """Resets failure counter upon successful verified adaptation."""
        breaker = self.get_or_create_breaker(tenant_id)
        breaker.consecutive_failures = 0
        if breaker.state == "HALF_OPEN":
            breaker.state = "CLOSED"
            control = self.get_or_create_control_state(tenant_id)
            control.circuit_breaker_state = "CLOSED"

    def activate_kill_switch(self, tenant_id: str, operator_id: str = "SOC_LEAD"):
        """Activates emergency kill switch (Section 49, 78)."""
        breaker = self.get_or_create_breaker(tenant_id)
        breaker.kill_switch_active = True
        control = self.get_or_create_control_state(tenant_id)
        control.kill_switch_active = True
        control.automation_enabled = False
        control.last_modified_by = operator_id
        control.updated_at = datetime.now(timezone.utc).isoformat()

    def deactivate_kill_switch(self, tenant_id: str, operator_id: str = "SOC_LEAD"):
        """Resumes automation from kill switch."""
        breaker = self.get_or_create_breaker(tenant_id)
        breaker.kill_switch_active = False
        control = self.get_or_create_control_state(tenant_id)
        control.kill_switch_active = False
        control.automation_enabled = True
        control.last_modified_by = operator_id
        control.updated_at = datetime.now(timezone.utc).isoformat()
