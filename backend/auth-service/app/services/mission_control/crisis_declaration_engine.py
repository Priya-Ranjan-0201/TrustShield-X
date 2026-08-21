"""
TruthShield X — Crisis Declaration Engine

Determines when an incident rises to crisis level based on configurable
policy thresholds. Never auto-declares without threshold evidence.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    CrisisDeclarationDTO,
    IncidentCommandDTO,
    BusinessServiceImpactDTO,
)


class CrisisDeclarationEngine:
    """Evaluates whether incident conditions meet crisis thresholds."""

    DEFAULT_THRESHOLDS = {
        "critical_services_affected": 2,
        "critical_incidents_active": 3,
        "data_exposure_detected": True,
        "control_failure_count": 3,
        "prolonged_outage_minutes": 30,
    }

    def __init__(self, thresholds: Optional[Dict[str, Any]] = None):
        self._thresholds = thresholds or self.DEFAULT_THRESHOLDS
        self._declarations: Dict[str, CrisisDeclarationDTO] = {}

    def evaluate_crisis(
        self,
        tenant_id: str,
        active_commands: List[IncidentCommandDTO],
        service_impacts: List[BusinessServiceImpactDTO],
        control_failures: int = 0,
        data_exposure_detected: bool = False,
    ) -> CrisisDeclarationDTO:
        """Evaluates crisis conditions against policy thresholds."""
        thresholds_met: List[str] = []

        critical_services = sum(
            1 for s in service_impacts
            if s.criticality == "CRITICAL" and s.availability_impact in ("TOTAL_OUTAGE", "DEGRADED")
        )
        if critical_services >= self._thresholds["critical_services_affected"]:
            thresholds_met.append(f"CRITICAL_SERVICES_AFFECTED: {critical_services}")

        crisis_incidents = sum(1 for c in active_commands if c.severity == "CRISIS")
        critical_incidents = sum(1 for c in active_commands if c.severity in ("CRITICAL", "CRISIS"))
        if critical_incidents >= self._thresholds["critical_incidents_active"]:
            thresholds_met.append(f"CRITICAL_INCIDENTS: {critical_incidents}")

        if data_exposure_detected and self._thresholds.get("data_exposure_detected"):
            thresholds_met.append("DATA_EXPOSURE_DETECTED")

        if control_failures >= self._thresholds["control_failure_count"]:
            thresholds_met.append(f"CONTROL_FAILURES: {control_failures}")

        is_crisis = len(thresholds_met) >= 2

        declaration = CrisisDeclarationDTO(
            tenant_id=tenant_id,
            incident_command_ids=[c.incident_command_id for c in active_commands],
            crisis_status="DECLARED" if is_crisis else "NOT_DECLARED",
            trigger_reason="; ".join(thresholds_met) if thresholds_met else "No thresholds met",
            policy_thresholds_met=thresholds_met,
            affected_services_count=critical_services,
            declared_by="CRISIS_DECLARATION_ENGINE",
            declared_at=datetime.now(timezone.utc).isoformat() if is_crisis else None,
        )

        if is_crisis:
            self._declarations[declaration.crisis_id] = declaration

        return declaration

    def get_crisis_status(self, tenant_id: str) -> str:
        """Returns current crisis status for a tenant."""
        for d in reversed(list(self._declarations.values())):
            if d.tenant_id == tenant_id and d.crisis_status == "DECLARED":
                return "DECLARED"
        return "NO_ACTIVE_CRISIS"

    def list_declarations(self, tenant_id: str) -> List[CrisisDeclarationDTO]:
        """Lists crisis declarations for a tenant."""
        return [d for d in self._declarations.values() if d.tenant_id == tenant_id]
