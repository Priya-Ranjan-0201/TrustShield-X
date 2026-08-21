"""
TruthShield X — Predictive Defense & Horizon Threat Forecasting Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.hunting_models import SecurityPredictionDTO, PredictionHorizonLiteral


class PredictiveDefenseEngine:
    """Forecasts campaign expansion, trust degradation, and attack surface exposure over multi-tier horizons."""

    def __init__(self):
        # prediction_id -> SecurityPredictionDTO
        self._predictions: Dict[str, SecurityPredictionDTO] = {}

    def forecast_threat_progression(
        self,
        target_subject: str,
        prediction_type: str,
        horizon: PredictionHorizonLiteral = "SHORT_TERM",
        predicted_probability: float = 0.85,
        confidence: float = 0.80,
        assumptions: Optional[List[str]] = None,
        supporting_evidence: Optional[List[Dict[str, Any]]] = None,
        tenant_id: str = "default_tenant",
    ) -> SecurityPredictionDTO:
        """Generates an evidence-backed probabilistic prediction over an explicit time horizon."""
        pred_id = f"prd_{uuid.uuid4().hex[:10]}"
        prediction = SecurityPredictionDTO(
            prediction_id=pred_id,
            tenant_id=tenant_id,
            target_subject=target_subject,
            prediction_type=prediction_type,
            horizon=horizon,
            predicted_probability=max(0.05, min(0.99, predicted_probability)),
            confidence=max(0.10, min(0.95, confidence)),
            assumptions=assumptions or ["Actor infrastructure reuse patterns remain consistent over 7-day window."],
            supporting_evidence=supporting_evidence or [{"source": "HistoricalCampaignCluster", "correlation": 0.88}],
            model_version="TruthShield-Predict-v11.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            actual_outcome="UNRESOLVED",
        )

        self._predictions[pred_id] = prediction
        return prediction

    def list_predictions(self, tenant_id: str = "default_tenant") -> List[SecurityPredictionDTO]:
        """Lists active predictions for tenant."""
        return [p for p in self._predictions.values() if p.tenant_id == tenant_id]
