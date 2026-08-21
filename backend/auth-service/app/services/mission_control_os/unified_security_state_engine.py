"""
TruthShield X — Unified Security State Engine (Phase 29).

Aggregates operational context across all security subsystems with explicit subsystem state ownership and conflict detection.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_os_models import UnifiedSecurityStateDTO, SecurityPostureDTO


class UnifiedSecurityStateEngine:
    """Aggregates unified operational mission state without overwriting subsystem sources of truth."""

    def __init__(self):
        self._current_state: Dict[str, UnifiedSecurityStateDTO] = {}
        self._seed_default_state()

    def _seed_default_state(self):
        s1 = UnifiedSecurityStateDTO(
            tenant_id="default_tenant",
            active_threats_count=1,
            active_campaigns_count=1,
            active_incidents_count=1,
            critical_alerts_count=2,
            compromised_assets_count=1,
            failing_controls_count=0,
            active_responses_count=1,
            active_recoveries_count=0,
            pending_tasks_count=3,
            state_conflicts_count=0,
            posture_summary=SecurityPostureDTO(),
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._current_state[s1.tenant_id] = s1

    def get_unified_state(self, tenant_id: str = "default_tenant") -> UnifiedSecurityStateDTO:
        if tenant_id not in self._current_state:
            s = UnifiedSecurityStateDTO(tenant_id=tenant_id)
            self._current_state[tenant_id] = s
        return self._current_state[tenant_id]

    def update_subsystem_metrics(
        self,
        tenant_id: str,
        active_threats: Optional[int] = None,
        active_incidents: Optional[int] = None,
        failing_controls: Optional[int] = None,
    ) -> UnifiedSecurityStateDTO:
        curr = self.get_unified_state(tenant_id)
        updated = UnifiedSecurityStateDTO(
            state_id=curr.state_id,
            tenant_id=tenant_id,
            active_threats_count=active_threats if active_threats is not None else curr.active_threats_count,
            active_campaigns_count=curr.active_campaigns_count,
            active_incidents_count=active_incidents if active_incidents is not None else curr.active_incidents_count,
            critical_alerts_count=curr.critical_alerts_count,
            compromised_assets_count=curr.compromised_assets_count,
            failing_controls_count=failing_controls if failing_controls is not None else curr.failing_controls_count,
            active_responses_count=curr.active_responses_count,
            active_recoveries_count=curr.active_recoveries_count,
            pending_tasks_count=curr.pending_tasks_count,
            state_conflicts_count=curr.state_conflicts_count,
            posture_summary=curr.posture_summary,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._current_state[tenant_id] = updated
        return updated
