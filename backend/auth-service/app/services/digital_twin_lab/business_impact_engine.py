"""
TruthShield X — Business Impact Engine (Phase 26).

Calculates business and operational disruption without fabricating unsupported financial loss figures.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.digital_twin_lab_models import BusinessImpactSimulationDTO


class BusinessImpactEngine:
    """Evaluates user disruption, downtime, and cascading downstream service degradation."""

    def __init__(self):
        self._impacts: Dict[str, BusinessImpactSimulationDTO] = {}

    def simulate_business_impact(
        self,
        scenario_id: str,
        affected_services: Optional[List[str]] = None,
        affected_users: int = 150,
        downtime_minutes: float = 4.5,
    ) -> BusinessImpactSimulationDTO:
        srvs = affected_services or ["srv_auth", "srv_scan"]
        cascade = ["srv_reports_export"] if "srv_auth" in srvs else []

        dto = BusinessImpactSimulationDTO(
            scenario_id=scenario_id,
            affected_services=srvs,
            affected_users=affected_users,
            service_downtime_minutes=downtime_minutes,
            data_availability_score=0.99,
            operational_impact_score=round(len(srvs) * 0.08, 2),
            recovery_effort_hours=1.0,
            cascade_failures=cascade,
            financial_impact_status="FINANCIAL_IMPACT_NOT_MODELED",
            claim_status="MODELED",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._impacts[dto.impact_id] = dto
        return dto

    def get_impact(self, impact_id: str) -> Optional[BusinessImpactSimulationDTO]:
        return self._impacts.get(impact_id)
