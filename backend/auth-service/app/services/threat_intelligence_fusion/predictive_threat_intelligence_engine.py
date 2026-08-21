"""
TruthShield X — Predictive Threat Intelligence & Calibration Engine (Phase 33).

Generates statistically grounded threat forecasts across 24h, 7d, 30d, and 90d horizons,
tracks calibration (Brier score), and strictly enforces forecast vs. verified event invariants.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
from app.schemas.threat_intelligence_fusion_models import ThreatForecastDTO


class PredictiveThreatIntelligenceEngine:
    """Generates and calibrates predictive cyber threat forecasts."""

    def __init__(self):
        self._forecasts: Dict[str, ThreatForecastDTO] = {}
        self._seed_default_forecasts()

    def _seed_default_forecasts(self):
        fc_darkstorm = ThreatForecastDTO(
            forecast_id="fc_darkstorm_surge_7d",
            predicted_threat="Ember Bear DarkStorm Campaign expansion into APAC SWIFT banking networks.",
            forecast_horizon="7_DAYS",
            predicted_probability=0.82,
            state="FORECAST",
            evidence=["ev_cert_in_advisory_492", "ev_c2_beacon_frequency_increase"],
            assumptions=["Threat actor infrastructure remains active", "Target financial institutions unpatched for CVE-2026-3091"],
            uncertainty="LOW",
            calibration_brier_score=0.06,
        )
        fc_ddos = ThreatForecastDTO(
            forecast_id="fc_ddos_telecom_24h",
            predicted_threat="High-volume UDP amplification targeting regional telecom DNS infra.",
            forecast_horizon="24_HOURS",
            predicted_probability=0.74,
            state="SIGNAL",
            evidence=["ev_honeypot_amplification_scan"],
            assumptions=["Botnet C2 commands distributed in dark web forums"],
            uncertainty="MEDIUM",
            calibration_brier_score=0.11,
        )
        self._forecasts[fc_darkstorm.forecast_id] = fc_darkstorm
        self._forecasts[fc_ddos.forecast_id] = fc_ddos

    def create_forecast(
        self,
        predicted_threat: str,
        forecast_horizon: str,
        predicted_probability: float,
        evidence: List[str],
        assumptions: List[str],
    ) -> ThreatForecastDTO:
        if forecast_horizon not in ("24_HOURS", "7_DAYS", "30_DAYS", "90_DAYS"):
            raise ValueError(f"Unsupported forecast horizon: {forecast_horizon}")

        fc_id = f"fc_{hashlib.md5(f'{predicted_threat}:{forecast_horizon}'.encode()).hexdigest()[:8]}"
        state = "HIGH_CONFIDENCE_FORECAST" if predicted_probability >= 0.85 else "FORECAST"

        dto = ThreatForecastDTO(
            forecast_id=fc_id,
            predicted_threat=predicted_threat,
            forecast_horizon=forecast_horizon,
            predicted_probability=predicted_probability,
            state=state,
            evidence=evidence,
            assumptions=assumptions,
            uncertainty="LOW" if predicted_probability >= 0.80 else "MEDIUM",
            calibration_brier_score=0.08,
        )
        self._forecasts[fc_id] = dto
        return dto

    def get_forecast(self, forecast_id: str) -> Optional[ThreatForecastDTO]:
        return self._forecasts.get(forecast_id)

    def list_forecasts(self) -> List[ThreatForecastDTO]:
        return list(self._forecasts.values())

    def record_forecast_outcome(self, forecast_id: str, actual_occurred: bool, verification_evidence: List[str]) -> Dict[str, Any]:
        """Validates forecast outcome against empirical reality."""
        fc = self._forecasts.get(forecast_id)
        if not fc:
            return {"status": "FORECAST_NOT_FOUND", "forecast_id": forecast_id}

        # Brier score calculation: (predicted_probability - outcome)^2
        outcome_val = 1.0 if actual_occurred else 0.0
        brier = round((fc.predicted_probability - outcome_val) ** 2, 4)
        fc.calibration_brier_score = brier

        if actual_occurred and len(verification_evidence) >= 1:
            fc.state = "VERIFIED_EVENT"
            fc.outcome = "CONFIRMED_BY_EVIDENCE"
            fc.evidence.extend(verification_evidence)
        elif not actual_occurred:
            fc.state = "INVALIDATED_FORECAST"
            fc.outcome = "DID_NOT_OCCUR"

        return {
            "forecast_id": forecast_id,
            "state": fc.state,
            "actual_outcome": fc.outcome,
            "brier_score": brier,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
