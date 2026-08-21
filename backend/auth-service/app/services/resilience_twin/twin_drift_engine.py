"""
TruthShield X — Reality-to-Twin Drift Engine (Phase 18).

Detects telemetry divergences where physical/cloud reality contradicts digital twin models.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.cyber_resilience_twin_models import TwinDriftEventDTO


class TwinDriftEngine:
    """Monitors discrepancies between runtime telemetry and modeled twin entities."""

    def __init__(self):
        # drift_id -> TwinDriftEventDTO
        self._drift_events: Dict[str, TwinDriftEventDTO] = {}

    def detect_drift(
        self,
        tenant_id: str,
        entity_id: str,
        reality_state: str,
        twin_state: str,
        severity: str = "MEDIUM",
    ) -> Optional[TwinDriftEventDTO]:
        """Flags drift when actual telemetry deviates from digital twin state."""
        if reality_state == twin_state:
            return None

        event = TwinDriftEventDTO(
            tenant_id=tenant_id,
            drift_type="REALITY_TO_TWIN_DRIFT",
            reality_state=f"{entity_id}: {reality_state}",
            twin_state=f"{entity_id}: {twin_state}",
            severity=severity,  # type: ignore
            status="DETECTED",
        )

        self._drift_events[event.drift_id] = event
        return event

    def list_drift_events(self, tenant_id: str = "default_tenant") -> List[TwinDriftEventDTO]:
        return [d for d in self._drift_events.values() if d.tenant_id == tenant_id]
