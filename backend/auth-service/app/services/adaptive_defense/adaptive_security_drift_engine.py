"""
TruthShield X — Adaptive Security Drift Engine (Phase 17).

Detects configuration, policy, identity, exposure, control, and infrastructure drift.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import (
    AdaptiveDriftEventDTO,
    DriftSeverityLiteral,
)


class AdaptiveSecurityDriftEngine:
    """Monitors environment baseline deviations and rates drift severity."""

    def __init__(self):
        self._drift_events: Dict[str, AdaptiveDriftEventDTO] = {}

    def record_drift(
        self,
        tenant_id: str,
        drift_type: str,
        affected_asset: str,
        previous_state: str,
        current_state: str,
        severity: DriftSeverityLiteral = "MEDIUM",
        exploitability: float = 0.5,
        business_criticality: str = "HIGH",
    ) -> AdaptiveDriftEventDTO:
        """Records and categorizes an observed security drift event."""
        drift = AdaptiveDriftEventDTO(
            tenant_id=tenant_id,
            drift_type=drift_type,  # type: ignore
            affected_asset=affected_asset,
            previous_state=previous_state,
            current_state=current_state,
            severity=severity,
            exploitability_factor=exploitability,
            business_criticality=business_criticality,
        )
        self._drift_events[drift.drift_id] = drift
        return drift

    def list_drift_events(self, tenant_id: str = "default_tenant") -> List[AdaptiveDriftEventDTO]:
        return [d for d in self._drift_events.values() if d.tenant_id == tenant_id]
