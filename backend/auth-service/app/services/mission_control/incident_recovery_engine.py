"""
TruthShield X — Incident Recovery Engine

Tracks recovery sequencing, dependency ordering, service health verification,
and residual risk calculation. Recovery is complete only when all verification
conditions are satisfied.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_models import IncidentRecoveryDTO


class IncidentRecoveryEngine:
    """Manages incident recovery lifecycle and residual risk assessment."""

    def __init__(self):
        self._recoveries: Dict[str, IncidentRecoveryDTO] = {}

    def initiate_recovery(
        self,
        incident_command_id: str,
        recovery_sequence: List[str],
        dependencies: Optional[List[str]] = None,
        pre_incident_risk: float = 15.0,
        incident_risk: float = 85.0,
    ) -> IncidentRecoveryDTO:
        """Initiates a recovery plan for an incident."""
        recovery = IncidentRecoveryDTO(
            incident_command_id=incident_command_id,
            recovery_sequence=recovery_sequence,
            dependencies=dependencies or [],
            pre_incident_risk=pre_incident_risk,
            incident_risk=incident_risk,
        )
        self._recoveries[recovery.recovery_id] = recovery
        return recovery

    def restore_service(self, recovery_id: str, service_id: str) -> IncidentRecoveryDTO:
        """Records a service restoration."""
        rec = self._recoveries.get(recovery_id)
        if not rec:
            raise ValueError(f"Recovery {recovery_id} not found.")
        if service_id not in rec.restored_services:
            rec.restored_services.append(service_id)
        return rec

    def restore_asset(self, recovery_id: str, asset_id: str) -> IncidentRecoveryDTO:
        """Records an asset restoration."""
        rec = self._recoveries.get(recovery_id)
        if not rec:
            raise ValueError(f"Recovery {recovery_id} not found.")
        if asset_id not in rec.restored_assets:
            rec.restored_assets.append(asset_id)
        return rec

    def verify_recovery(
        self,
        recovery_id: str,
        service_health_verified: bool = False,
        security_controls_verified: bool = False,
        monitoring_restored: bool = False,
        audit_restored: bool = False,
        tenant_isolation_verified: bool = False,
        post_response_risk: float = 20.0,
    ) -> IncidentRecoveryDTO:
        """Validates recovery conditions and calculates residual risk."""
        rec = self._recoveries.get(recovery_id)
        if not rec:
            raise ValueError(f"Recovery {recovery_id} not found.")

        rec.service_health_verified = service_health_verified
        rec.security_controls_verified = security_controls_verified
        rec.monitoring_restored = monitoring_restored
        rec.audit_restored = audit_restored
        rec.tenant_isolation_verified = tenant_isolation_verified
        rec.post_response_risk = post_response_risk
        rec.residual_risk = max(0.0, post_response_risk - rec.pre_incident_risk)
        rec.verified_at = datetime.now(timezone.utc).isoformat()

        # Recovery is complete only when ALL conditions are verified
        rec.recovery_complete = all([
            service_health_verified,
            security_controls_verified,
            monitoring_restored,
            audit_restored,
            tenant_isolation_verified,
        ])

        return rec

    def get_recovery(self, recovery_id: str) -> Optional[IncidentRecoveryDTO]:
        """Retrieves a recovery record."""
        return self._recoveries.get(recovery_id)

    def is_recovery_complete(self, recovery_id: str) -> bool:
        """Returns whether recovery is verified complete."""
        rec = self._recoveries.get(recovery_id)
        return rec.recovery_complete if rec else False
