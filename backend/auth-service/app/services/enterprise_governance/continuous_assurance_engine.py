"""
TruthShield X — Continuous Assurance Engine (Phase 32).

Reevaluates control effectiveness on events, system changes, incidents, and generates COMPLIANCE_DRIFT on regressions.
"""

from typing import Dict, List, Any
from app.schemas.enterprise_governance_models import ComplianceDriftEventDTO


class ContinuousAssuranceEngine:
    """Continuously reassesses control posture upon configuration changes and security telemetry events."""

    def __init__(self):
        self._drift_events: List[ComplianceDriftEventDTO] = []

    def trigger_change_based_reassessment(
        self,
        control_id: str,
        system_change_event: str,
        control_still_effective: bool,
    ) -> Dict[str, Any]:
        if not control_still_effective:
            drift = ComplianceDriftEventDTO(
                control_id=control_id,
                previous_state="VERIFIED",
                current_state="DEGRADED",
                severity="HIGH",
            )
            self._drift_events.append(drift)
            return {
                "control_id": control_id,
                "status": "COMPLIANCE_DRIFT",
                "assurance_verdict": "DEGRADED",
                "action_required": "OPEN_REMEDIATION_TASK",
                "drift_event": drift,
            }

        return {
            "control_id": control_id,
            "status": "ASSURANCE_MAINTAINED",
            "assurance_verdict": "EFFECTIVE",
            "action_required": "NONE",
            "drift_event": None,
        }

    def list_drift_events(self) -> List[ComplianceDriftEventDTO]:
        return list(self._drift_events)
