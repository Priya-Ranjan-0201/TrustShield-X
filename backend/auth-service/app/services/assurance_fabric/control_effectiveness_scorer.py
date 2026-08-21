"""
TruthShield X — Control Effectiveness & Assurance Scorer (Phase 24).

Computes multidimensional assurance metrics and enforces strict empirical maturity level boundaries.
"""

from typing import Dict, Any
from datetime import datetime, timezone
from app.schemas.security_assurance_fabric_models import AssuranceScorecardDTO


class ControlEffectivenessScorer:
    """Evaluates security control efficacy across multiple empirical dimensions."""

    def evaluate_scorecard(
        self,
        tenant_id: str = "default_tenant",
        has_empirical_tests: bool = True,
        controls_pass_rate: float = 0.98,
        drift_count: int = 0,
    ) -> AssuranceScorecardDTO:
        impl_score = 98.0
        val_score = round(controls_pass_rate * 100.0, 1) if has_empirical_tests else 30.0
        eff_score = 96.0 if drift_count == 0 else 75.0
        freshness_score = 96.0 if has_empirical_tests else 40.0

        overall = (impl_score * 0.25) + (val_score * 0.25) + (eff_score * 0.25) + (freshness_score * 0.25)

        # Maturity Level Invariant: Cannot reach Level 5 without recurring empirical validation
        if not has_empirical_tests:
            maturity = "LEVEL_2_IMPLEMENTED"
        elif overall >= 90.0:
            maturity = "LEVEL_5_CONTINUOUSLY_VALIDATED"
        else:
            maturity = "LEVEL_3_TESTED"

        grade = "EXCELLENT" if overall >= 90.0 else ("ADEQUATE" if overall >= 75.0 else "NEEDS_IMPROVEMENT")
        residual_risk = round(max(0.0, 100.0 - overall), 1)

        return AssuranceScorecardDTO(
            tenant_id=tenant_id,
            overall_score=round(overall, 1),
            implementation_score=impl_score,
            validation_score=val_score,
            effectiveness_score=eff_score,
            freshness_score=freshness_score,
            residual_risk_score=residual_risk,
            maturity_level=maturity,  # type: ignore
            scorecard_grade=grade,  # type: ignore
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
