"""
TruthShield X — Threat Velocity Engine (Phase 27).

Calculates time-series rates of change for indicators, campaign infrastructure, and targeting activity.
"""

from typing import Dict, Any


class ThreatVelocityEngine:
    """Measures acceleration and deceleration of threat events across time windows."""

    def calculate_velocity(self, campaign_id: str, new_indicators_24h: int, baseline_indicators_daily: int = 5) -> Dict[str, Any]:
        growth_rate = round((new_indicators_24h - baseline_indicators_daily) / max(1, baseline_indicators_daily), 2)
        is_surge = growth_rate > 1.5

        return {
            "campaign_id": campaign_id,
            "new_indicators_24h": new_indicators_24h,
            "baseline_daily_rate": baseline_indicators_daily,
            "growth_rate_metric": growth_rate,
            "velocity_surge_detected": is_surge,
            "status": "SURGE" if is_surge else "NOMINAL",
            "claim_status": "OBSERVED",
        }
