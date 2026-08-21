"""
TruthShield X — Resilience Gap Engine (Phase 23).

Identifies vulnerabilities in business continuity, untested recovery paths, and stale backups.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_resilience_models import ResilienceGapDTO


class ResilienceGapEngine:
    """Discovers architectural and procedural resilience gaps."""

    def __init__(self):
        self._gaps: Dict[str, ResilienceGapDTO] = {}
        self._seed_default_gaps()

    def _seed_default_gaps(self):
        g1 = ResilienceGapDTO(
            gap_id="gap_untested_redis_failover",
            tenant_id="default_tenant",
            gap_type="UNVERIFIED_FAILOVER",
            severity="HIGH",
            affected_service="svc_checkout_api",
            evidence="Redis Multi-AZ failover has not been tested in sandbox during the last 90 days.",
            recommendation="Schedule an automated staging failover drill using DisasterRecoveryDrillEngine.",
            validation_status="UNRESOLVED",
        )
        self._gaps[g1.gap_id] = g1

    def detect_gaps(self, backup_age_hours: float, failover_tested: bool) -> List[ResilienceGapDTO]:
        detected = []
        if backup_age_hours > 24.0:
            g = ResilienceGapDTO(
                gap_type="STALE_BACKUP",
                severity="CRITICAL",
                affected_service="ast_pg_primary",
                evidence=f"Last valid backup is {backup_age_hours} hours old (> 24h threshold).",
                recommendation="Trigger immediate automated full snapshot and investigate backup cron.",
            )
            detected.append(g)
            self._gaps[g.gap_id] = g

        if not failover_tested:
            g2 = ResilienceGapDTO(
                gap_type="UNTESTED_BACKUP",
                severity="HIGH",
                affected_service="ast_api_gateway",
                evidence="Secondary region active-active failover is untested.",
                recommendation="Execute non-destructive staging failover verification.",
            )
            detected.append(g2)
            self._gaps[g2.gap_id] = g2

        return detected

    def list_gaps(self, tenant_id: str = "default_tenant") -> List[ResilienceGapDTO]:
        return list(self._gaps.values())
