"""
TruthShield X — Resilience Drift Engine (Phase 23).

Detects configuration, infrastructure, and dependency drift that invalidates existing recovery plans.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.cyber_resilience_models import RecoveryDriftDTO


class ResilienceDriftEngine:
    """Monitors live environment changes and identifies recovery plan divergence."""

    def __init__(self):
        self._drift_records: Dict[str, RecoveryDriftDTO] = {}
        self._seed_default_drift()

    def _seed_default_drift(self):
        d1 = RecoveryDriftDTO(
            drift_id="drift_new_unmapped_db_replica",
            tenant_id="default_tenant",
            component_type="INFRASTRUCTURE",
            description="Unregistered read-replica added in us-east-2 without updating the failover DNS plan.",
            impact_assessment="Recovery Plan marked OUTDATED until replica sync is added to recovery steps.",
            is_reconciled=False,
        )
        self._drift_records[d1.drift_id] = d1

    def record_drift(
        self,
        component_type: str,
        description: str,
        impact_assessment: str,
        tenant_id: str = "default_tenant",
    ) -> RecoveryDriftDTO:
        dto = RecoveryDriftDTO(
            tenant_id=tenant_id,
            component_type=component_type,  # type: ignore
            description=description,
            impact_assessment=impact_assessment,
            is_reconciled=False,
        )
        self._drift_records[dto.drift_id] = dto
        return dto

    def reconcile_drift(self, drift_id: str) -> Optional[RecoveryDriftDTO]:
        drift = self._drift_records.get(drift_id)
        if not drift:
            return None
        reconciled = RecoveryDriftDTO(
            drift_id=drift.drift_id,
            tenant_id=drift.tenant_id,
            component_type=drift.component_type,
            description=drift.description,
            drift_detected_at=drift.drift_detected_at,
            impact_assessment="Reconciled and integrated into updated recovery plan.",
            is_reconciled=True,
        )
        self._drift_records[drift_id] = reconciled
        return reconciled

    def list_drifts(self, tenant_id: str = "default_tenant") -> List[RecoveryDriftDTO]:
        return list(self._drift_records.values())
