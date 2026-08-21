"""
TruthShield X — Security Drift Engine (Phase 24).

Detects configuration, authorization, detection, playbook, recovery, model, and data drift across environments.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import SecurityDriftDTO, DriftTypeLiteral


class SecurityDriftEngine:
    """Identifies unauthorized, unintended, or undocumented shifts in security posture."""

    def __init__(self):
        self._drift_records: Dict[str, SecurityDriftDTO] = {}
        self._seed_default_drift()

    def _seed_default_drift(self):
        d1 = SecurityDriftDTO(
            drift_id="sdrift_authz_role_expansion",
            tenant_id="default_tenant",
            drift_type="AUTHORIZATION",
            component="role_soc_analyst",
            description="Wildcard action permission added to SOC Analyst role without change ticket.",
            is_reconciled=False,
        )
        self._drift_records[d1.drift_id] = d1

    def detect_drift(
        self,
        drift_type: DriftTypeLiteral,
        component: str,
        description: str,
        tenant_id: str = "default_tenant",
    ) -> SecurityDriftDTO:
        dto = SecurityDriftDTO(
            tenant_id=tenant_id,
            drift_type=drift_type,
            component=component,
            description=description,
            is_reconciled=False,
        )
        self._drift_records[dto.drift_id] = dto
        return dto

    def reconcile_drift(self, drift_id: str, notes: str = "Reconciled via policy revert.") -> Optional[SecurityDriftDTO]:
        drift = self._drift_records.get(drift_id)
        if not drift:
            return None
        reconciled = SecurityDriftDTO(
            drift_id=drift.drift_id,
            tenant_id=drift.tenant_id,
            drift_type=drift.drift_type,
            component=drift.component,
            description=drift.description,
            detected_at=drift.detected_at,
            is_reconciled=True,
            reconciliation_notes=notes,
        )
        self._drift_records[drift_id] = reconciled
        return reconciled

    def list_drifts(self, tenant_id: str = "default_tenant") -> List[SecurityDriftDTO]:
        return list(self._drift_records.values())
