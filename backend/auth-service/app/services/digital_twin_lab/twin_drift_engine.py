"""
TruthShield X — Twin Drift Engine (Phase 26).

Detects discrepancy between live observed telemetry and the internal Digital Twin representation.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.digital_twin_lab_models import TwinDriftRecordDTO, DriftCategoryLiteral


class TwinDriftEngine:
    """Identifies and tracks drift between real environment and digital twin."""

    def __init__(self):
        self._drifts: Dict[str, TwinDriftRecordDTO] = {}
        self._seed_default_drift()

    def _seed_default_drift(self):
        d1 = TwinDriftRecordDTO(
            drift_id="twdr_api_ratelimit_drift",
            tenant_id="default_tenant",
            drift_category="CONFIGURATION_DRIFT",
            observed_difference="Live API gateway rate-limit threshold differs from Digital Twin model.",
            severity="MEDIUM",
            is_reconciled=False,
        )
        self._drifts[d1.drift_id] = d1

    def detect_drift(
        self,
        drift_category: DriftCategoryLiteral,
        difference_details: str,
        severity: str = "MEDIUM",
        tenant_id: str = "default_tenant",
    ) -> TwinDriftRecordDTO:
        dto = TwinDriftRecordDTO(
            tenant_id=tenant_id,
            drift_category=drift_category,
            observed_difference=difference_details,
            severity=severity,  # type: ignore
            is_reconciled=False,
        )
        self._drifts[dto.drift_id] = dto
        return dto

    def reconcile_drift(self, drift_id: str) -> Optional[TwinDriftRecordDTO]:
        drift = self._drifts.get(drift_id)
        if not drift:
            return None
        reconciled = TwinDriftRecordDTO(
            drift_id=drift.drift_id,
            tenant_id=drift.tenant_id,
            drift_category=drift.drift_category,
            observed_difference=drift.observed_difference,
            severity=drift.severity,
            synchronized_at=datetime.now(timezone.utc).isoformat(),
            is_reconciled=True,
        )
        self._drifts[drift_id] = reconciled
        return reconciled

    def list_drifts(self, tenant_id: str = "default_tenant") -> List[TwinDriftRecordDTO]:
        return list(self._drifts.values())
