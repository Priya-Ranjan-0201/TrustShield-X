"""
TruthShield X — Disaster Recovery Drill Engine (Phase 23).

Coordinates controlled DR exercises across environments with strict abort conditions and safety controls.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.cyber_resilience_models import DisasterRecoveryDrillDTO, DrillTypeLiteral


class DisasterRecoveryDrillEngine:
    """Orchestrates tabletop, simulated, and staging disaster recovery exercises."""

    def __init__(self):
        self._drills: Dict[str, DisasterRecoveryDrillDTO] = {}
        self._seed_default_drill()

    def _seed_default_drill(self):
        d1 = DisasterRecoveryDrillDTO(
            drill_id="drill_db_restore_staging",
            tenant_id="default_tenant",
            drill_type="DATABASE_RESTORE",
            environment="ISOLATED_SANDBOX",
            scope="SANDBOX_CHECKOUT_RESTORE",
            status="COMPLETED",
            measured_rto_minutes=14.5,
            measured_rpo_minutes=4.2,
            evidence_ids=["ev_drill_pg_01", "ev_drill_pg_02"],
        )
        self._drills[d1.drill_id] = d1

    def schedule_drill(
        self,
        drill_type: DrillTypeLiteral,
        environment: str = "ISOLATED_SANDBOX",
        scope: str = "SANDBOX_FAILOVER_TEST",
        tenant_id: str = "default_tenant",
    ) -> DisasterRecoveryDrillDTO:
        # Drill safety check: Production destructive testing blocked
        if environment == "PRODUCTION":
            raise ValueError("Drill Safety Violation: Destructive drills against PRODUCTION are strictly prohibited.")

        dto = DisasterRecoveryDrillDTO(
            tenant_id=tenant_id,
            drill_type=drill_type,
            environment=environment,  # type: ignore
            scope=scope,
            status="RUNNING",
            started_at=datetime.now(timezone.utc).isoformat(),
            completed_at=None,
        )
        self._drills[dto.drill_id] = dto
        return dto

    def abort_drill(self, drill_id: str, reason: str) -> DisasterRecoveryDrillDTO:
        drill = self._drills.get(drill_id)
        if not drill:
            raise ValueError(f"Drill '{drill_id}' not found.")

        aborted = DisasterRecoveryDrillDTO(
            drill_id=drill.drill_id,
            tenant_id=drill.tenant_id,
            drill_type=drill.drill_type,
            environment=drill.environment,
            scope=drill.scope,
            status="ABORTED",
            abort_reason=reason,
            started_at=drill.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            measured_rto_minutes=0.0,
            measured_rpo_minutes=0.0,
        )
        self._drills[drill_id] = aborted
        return aborted

    def complete_drill(self, drill_id: str, measured_rto: float, measured_rpo: float) -> DisasterRecoveryDrillDTO:
        drill = self._drills.get(drill_id)
        if not drill:
            raise ValueError(f"Drill '{drill_id}' not found.")

        completed = DisasterRecoveryDrillDTO(
            drill_id=drill.drill_id,
            tenant_id=drill.tenant_id,
            drill_type=drill.drill_type,
            environment=drill.environment,
            scope=drill.scope,
            status="COMPLETED",
            started_at=drill.started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            measured_rto_minutes=measured_rto,
            measured_rpo_minutes=measured_rpo,
        )
        self._drills[drill_id] = completed
        return completed

    def list_drills(self, tenant_id: str = "default_tenant") -> List[DisasterRecoveryDrillDTO]:
        return list(self._drills.values())
