"""
TruthShield X — Security Assurance Score & Summary Engine
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.assurance_models import (
    SecurityControlRegistryDTO,
    SecurityAssuranceSummaryDTO,
)


class SecurityAssuranceScoreEngine:
    """Calculates multidimensional weighted security assurance and certification metrics."""

    def calculate_summary(
        self,
        controls: List[SecurityControlRegistryDTO],
        active_drifts_count: int = 0,
        invariants_violated_count: int = 0,
    ) -> SecurityAssuranceSummaryDTO:
        """Computes platform assurance coverage and weighted security score."""
        total = len(controls)
        if total == 0:
            return SecurityAssuranceSummaryDTO(
                overall_assurance_score=0.0,
                control_coverage_percentage=0.0,
                total_controls=0,
                controls_verified=0,
                controls_degraded=0,
                controls_failed=0,
                controls_unknown=0,
                active_drifts_count=active_drifts_count,
                invariants_satisfied_count=5,
                invariants_violated_count=invariants_violated_count,
            )

        verified = sum(1 for c in controls if c.verification_state == "VERIFIED")
        degraded = sum(1 for c in controls if c.verification_state == "DEGRADED")
        failed = sum(1 for c in controls if c.verification_state == "FAILED")
        unknown = sum(1 for c in controls if c.verification_state in ("UNKNOWN", "DOCUMENTED", "CONFIGURED"))

        coverage = (verified / total) * 100.0

        # Weighted calculation
        base_score = (verified * 1.0 + degraded * 0.5 + unknown * 0.2) / total * 100.0
        # Penalties for active drifts and invariant violations
        penalties = (active_drifts_count * 5.0) + (invariants_violated_count * 25.0)
        overall_score = max(0.0, min(100.0, base_score - penalties))

        return SecurityAssuranceSummaryDTO(
            overall_assurance_score=round(overall_score, 1),
            control_coverage_percentage=round(coverage, 1),
            total_controls=total,
            controls_verified=verified,
            controls_degraded=degraded,
            controls_failed=failed,
            controls_unknown=unknown,
            active_drifts_count=active_drifts_count,
            invariants_satisfied_count=5 - invariants_violated_count,
            invariants_violated_count=invariants_violated_count,
            last_certified_at=datetime.now(timezone.utc).isoformat(),
        )
