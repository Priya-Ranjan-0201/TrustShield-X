"""
TruthShield X — Governance Posture Score Engine
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.governance_fabric_models import (
    GovernancePostureSummaryDTO,
    GovernanceRequirementDTO,
    GovernanceExceptionDTO,
    GovernanceEvidenceDTO,
)


class GovernancePostureEngine:
    """Computes comprehensive continuous governance posture and compliance confidence."""

    def calculate_posture(
        self,
        frameworks_count: int,
        requirements: List[GovernanceRequirementDTO],
        exceptions: List[GovernanceExceptionDTO],
        evidence_list: List[GovernanceEvidenceDTO],
    ) -> GovernancePostureSummaryDTO:
        """Calculates multi-dimensional governance posture summary."""
        total_reqs = len(requirements)
        if total_reqs == 0:
            return GovernancePostureSummaryDTO(
                governance_posture_score=0.0,
                compliance_confidence=0.0,
                total_frameworks=frameworks_count,
                total_requirements=0,
                requirements_satisfied=0,
                requirements_partial=0,
                requirements_not_satisfied=0,
                active_exceptions=0,
                expired_exceptions=0,
                active_remediations=0,
                stale_evidence_count=0,
            )

        satisfied = sum(1 for r in requirements if r.status == "SATISFIED")
        partial = sum(1 for r in requirements if r.status == "PARTIALLY_SATISFIED")
        not_sat = sum(1 for r in requirements if r.status == "NOT_SATISFIED")

        active_exps = sum(1 for e in exceptions if e.status == "ACTIVE")
        expired_exps = sum(1 for e in exceptions if e.status == "EXPIRED")

        stale_ev = sum(1 for e in evidence_list if e.freshness in ("STALE", "EXPIRED", "INVALID"))

        base_score = (satisfied * 1.0 + partial * 0.5) / total_reqs * 100.0
        penalties = (expired_exps * 10.0) + (stale_ev * 5.0)
        final_score = max(0.0, min(100.0, base_score - penalties))

        confidence = 0.95 if stale_ev == 0 else max(0.40, 0.95 - (stale_ev * 0.10))

        return GovernancePostureSummaryDTO(
            governance_posture_score=round(final_score, 1),
            compliance_confidence=round(confidence, 2),
            total_frameworks=frameworks_count,
            total_requirements=total_reqs,
            requirements_satisfied=satisfied,
            requirements_partial=partial,
            requirements_not_satisfied=not_sat,
            active_exceptions=active_exps,
            expired_exceptions=expired_exps,
            active_remediations=not_sat,
            stale_evidence_count=stale_ev,
            last_assessed_at=datetime.now(timezone.utc).isoformat(),
        )
