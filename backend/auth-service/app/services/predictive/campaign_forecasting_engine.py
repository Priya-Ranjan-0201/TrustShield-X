"""Campaign Growth & Forecasting Engine (Phase 6 - Sections 7, 12, 16, 17).

Analyzes campaign expansion velocity, predicts growth states (ACCELERATING, STABLE, DECLINING, DORMANT, REACTIVATED),
estimates conservative next-stage activity, and balances predictions with counter-evidence.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.predictive_threat_models import (
    CampaignForecastDTO,
    CampaignGrowthStateLiteral,
    PredictionConfidenceLiteral,
)


class CampaignForecastingEngine:
    """Generates conservative, evidence-grounded forecasts of campaign expansion."""

    def __init__(self):
        self._forecasts: Dict[str, CampaignForecastDTO] = {}

    def forecast_campaign(
        self,
        campaign_id: str,
        entity_count: int,
        daily_growth_rate: float,
        current_risk: float = 75.0,
        has_counter_evidence: bool = False,
        supporting_signals: Optional[List[str]] = None,
    ) -> CampaignForecastDTO:
        """Forecasts campaign expansion state, projected risk, and potential next-stage activities."""
        # 1. Determine Growth State
        if daily_growth_rate >= 1.50:
            growth_state: CampaignGrowthStateLiteral = "ACCELERATING"
            projected_risk = min(100.0, current_risk + 18.0)
            next_events = [
                "Potential rotation to fresh C2 fallback domains within 48 hours",
                "Potential expansion of phishing SMS distribution radius",
            ]
        elif daily_growth_rate >= 0.80:
            growth_state = "STABLE"
            projected_risk = min(100.0, current_risk + 5.0)
            next_events = [
                "Potential persistence on existing verified infrastructure",
            ]
        elif daily_growth_rate > 0.0:
            growth_state = "DECLINING"
            projected_risk = max(10.0, current_risk - 10.0)
            next_events = [
                "Potential abandonment of blocked endpoints",
            ]
        else:
            growth_state = "DORMANT"
            projected_risk = max(10.0, current_risk - 25.0)
            next_events = [
                "No imminent expansion activity predicted based on inactive telemetry",
            ]

        # 2. Balance with Counter-Evidence (Section 17)
        counter_list = []
        if has_counter_evidence:
            counter_list.append("Shared CDN hosting infrastructure reduces attribution certainty")
            # Discount confidence when counter-evidence is present
            confidence: PredictionConfidenceLiteral = "LOW"
        else:
            confidence = "MEDIUM" if daily_growth_rate >= 1.50 else "LOW"

        forecast_id = f"fcst_{uuid.uuid4().hex[:12]}"
        signals = supporting_signals or [f"daily_growth_rate:{daily_growth_rate}", f"entity_count:{entity_count}"]

        forecast = CampaignForecastDTO(
            forecast_id=forecast_id,
            campaign_id=campaign_id,
            growth_state=growth_state,
            current_size=entity_count,
            projected_growth_rate=daily_growth_rate,
            current_risk=current_risk,
            projected_risk=projected_risk,
            confidence=confidence,
            possible_next_events=next_events,
            supporting_signals=signals,
            counter_evidence=counter_list,
            time_horizon="72H",
            limitations=[
                "Forecast assumes adversary operational patterns adhere to historical infrastructure lifecycles",
            ],
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

        self._forecasts[campaign_id] = forecast
        return forecast

    def get_campaign_forecast(self, campaign_id: str) -> Optional[CampaignForecastDTO]:
        """Retrieves stored forecast for a campaign."""
        return self._forecasts.get(campaign_id)
