"""Predictive Risk Engine (Phase 6 - Section 11, 26).

Calculates projected risk alongside current observed risk without overwriting actual observations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.schemas.predictive_threat_models import PredictiveRiskDTO


class PredictiveRiskEngine:
    """Calculates forward-looking predictive risk deltas based on velocity, anomalies, and feed reliability."""

    def calculate_predictive_risk(
        self,
        entity_or_campaign_id: str,
        current_observed_risk: float,
        campaign_velocity: float = 1.0,
        anomaly_z_score: float = 0.0,
        source_reliability: float = 0.85,
        time_horizon: str = "24H",
    ) -> PredictiveRiskDTO:
        """Calculates projected risk delta."""
        # Risk projection model:
        # velocity factor (0 to 15 pts) + anomaly factor (0 to 20 pts)
        velocity_delta = max(0.0, min(15.0, (campaign_velocity - 1.0) * 10.0))
        anomaly_delta = max(0.0, min(20.0, anomaly_z_score * 4.0))

        raw_delta = (velocity_delta + anomaly_delta) * source_reliability
        projected_risk = min(100.0, max(0.0, current_observed_risk + raw_delta))
        confidence = min(0.95, max(0.40, source_reliability * 0.90))

        supporting = []
        if velocity_delta > 0:
            supporting.append(f"Campaign expansion velocity ({campaign_velocity:.2f}x) adds {velocity_delta:.1f} pts")
        if anomaly_delta > 0:
            supporting.append(f"Telemetry burst anomaly (z={anomaly_z_score:.2f}) adds {anomaly_delta:.1f} pts")

        return PredictiveRiskDTO(
            entity_or_campaign_id=entity_or_campaign_id,
            current_observed_risk=round(current_observed_risk, 1),
            projected_risk=round(projected_risk, 1),
            prediction_confidence=round(confidence, 2),
            risk_delta=round(projected_risk - current_observed_risk, 1),
            time_horizon=time_horizon,
            supporting_factors=supporting,
            counter_factors=[],
            limitations=[
                "Observed risk remains the authoritative baseline for automated governance controls",
            ],
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )
