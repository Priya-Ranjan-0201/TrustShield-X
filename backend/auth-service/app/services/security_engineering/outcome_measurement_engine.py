"""
TruthShield X — Outcome Measurement Engine (Phase 25).

Empirically compares pre-change baselines against post-change telemetry to quantify real security gain.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
from app.schemas.security_engineering_models import OutcomeMeasurementDTO, OutcomeStatusLiteral


class OutcomeMeasurementEngine:
    """Measures empirical delta between pre-change baseline and actual post-change observation."""

    def __init__(self):
        self._outcomes: Dict[str, OutcomeMeasurementDTO] = {}

    def measure_outcome(
        self,
        improvement_id: str,
        baseline_metric: float,
        expected_metric: float,
        actual_metric: float,
        metric_direction: str = "LOWER_IS_BETTER",  # or HIGHER_IS_BETTER
    ) -> OutcomeMeasurementDTO:
        if metric_direction == "LOWER_IS_BETTER":
            if actual_metric < baseline_metric:
                status: OutcomeStatusLiteral = "IMPROVED"
            elif actual_metric == baseline_metric:
                status = "UNCHANGED"
            else:
                status = "DEGRADED"
        else:
            if actual_metric > baseline_metric:
                status = "IMPROVED"
            elif actual_metric == baseline_metric:
                status = "UNCHANGED"
            else:
                status = "DEGRADED"

        risk_reduction = round(abs(baseline_metric - actual_metric) * 100.0, 1)

        dto = OutcomeMeasurementDTO(
            improvement_id=improvement_id,
            baseline_metric=baseline_metric,
            expected_metric=expected_metric,
            actual_metric=actual_metric,
            outcome_status=status,
            risk_reduction_score=risk_reduction,
            measured_at=datetime.now(timezone.utc).isoformat(),
        )
        self._outcomes[dto.outcome_id] = dto
        return dto

    def get_outcome(self, outcome_id: str) -> Optional[OutcomeMeasurementDTO]:
        return self._outcomes.get(outcome_id)
