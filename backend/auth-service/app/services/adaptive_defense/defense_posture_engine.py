"""
TruthShield X — Defense Posture Engine (Phase 17).

Manages real-time evidence-driven defense posture states across tenant environments.
"""

from typing import Dict, Optional, List
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import (
    DefensePostureDTO,
    DefensePostureStateLiteral,
)


class DefensePostureEngine:
    """Calculates and maintains tenant defense posture state transitions."""

    def __init__(self):
        # tenant_id -> DefensePostureDTO
        self._postures: Dict[str, DefensePostureDTO] = {}

    def get_or_create_posture(self, tenant_id: str = "default_tenant", environment: str = "PRODUCTION") -> DefensePostureDTO:
        """Retrieves or initializes a defense posture for a tenant."""
        if tenant_id not in self._postures:
            self._postures[tenant_id] = DefensePostureDTO(
                tenant_id=tenant_id,
                environment=environment,
            )
        return self._postures[tenant_id]

    def update_posture(
        self,
        tenant_id: str,
        threat_level: str = "LOW",
        active_incidents: int = 0,
        active_campaigns: int = 0,
        control_health: float = 0.95,
        exposure_level: float = 0.15,
        attack_surface_score: float = 24.5,
    ) -> DefensePostureDTO:
        """Evaluates and transitions defense posture based on telemetry."""
        posture = self.get_or_create_posture(tenant_id)

        # Evidence-driven state transitions (Section 4)
        if active_incidents >= 3 or threat_level == "CRITICAL":
            new_state: DefensePostureStateLiteral = "CRITICAL"
        elif active_incidents >= 1 or active_campaigns >= 2 or threat_level == "HIGH":
            new_state = "HIGH_ALERT"
        elif active_campaigns >= 1 or threat_level == "ELEVATED" or exposure_level > 0.40:
            new_state = "ELEVATED"
        elif control_health < 0.60:
            new_state = "DEGRADED"
        else:
            new_state = "NORMAL"

        posture.security_state = new_state
        posture.threat_level = threat_level  # type: ignore
        posture.active_incidents_count = active_incidents
        posture.active_campaigns_count = active_campaigns
        posture.control_health = control_health
        posture.exposure_level = exposure_level
        posture.attack_surface_score = attack_surface_score
        posture.posture_version += 1
        posture.last_verified = datetime.now(timezone.utc).isoformat()

        return posture

    def list_postures(self) -> List[DefensePostureDTO]:
        return list(self._postures.values())
