"""FastAPI Endpoints for Predictive Threat Intelligence, Threat Hunting & Early Warning (Phase 6)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel

from app.schemas.predictive_threat_models import (
    ThreatSignalDTO,
    EarlyWarningDTO,
    CampaignForecastDTO,
    PredictiveRiskDTO,
    ThreatHuntQueryDTO,
    ThreatHuntResultDTO,
    ThreatAnomalyDTO,
    PredictionCalibrationRecordDTO,
)
from app.services.predictive.threat_signal_normalization_service import ThreatSignalNormalizationService
from app.services.predictive.threat_feed_quality_engine import ThreatFeedQualityEngine
from app.services.predictive.threat_anomaly_engine import ThreatAnomalyEngine
from app.services.predictive.early_warning_engine import EarlyWarningEngine
from app.services.predictive.campaign_forecasting_engine import CampaignForecastingEngine
from app.services.predictive.predictive_risk_engine import PredictiveRiskEngine
from app.services.predictive.threat_hunting_engine import ThreatHuntingEngine
from app.services.predictive.prediction_calibration_engine import PredictionCalibrationEngine

router = APIRouter(prefix="/threat-intelligence-predictive", tags=["Predictive Threat Intelligence & Early Warning"])

# Service singletons
_signal_service = ThreatSignalNormalizationService()
_feed_quality = ThreatFeedQualityEngine()
_anomaly_engine = ThreatAnomalyEngine()
_warning_engine = EarlyWarningEngine()
_forecast_engine = CampaignForecastingEngine()
_predictive_risk = PredictiveRiskEngine()
_hunt_engine = ThreatHuntingEngine()
_calibration_engine = PredictionCalibrationEngine()


# ---------------------------------------------------------------------------
# Threat Signals & Early Warnings
# ---------------------------------------------------------------------------

@router.get("/signals", response_model=List[ThreatSignalDTO])
async def get_threat_signals(
    entity_id: Optional[str] = None,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves threat signals for an entity or tenant."""
    if entity_id:
        return _signal_service.get_signals_for_entity(entity_id, tenant_id)
    return []


@router.get("/warnings", response_model=List[EarlyWarningDTO])
async def get_early_warnings(tenant_id: str = Query("default_tenant")):
    """Retrieves active early-warning alerts for emerging campaigns or infrastructure expansion."""
    return _warning_engine.list_warnings(tenant_id)


# ---------------------------------------------------------------------------
# Predictions & Forecasts
# ---------------------------------------------------------------------------

@router.get("/predictions/{prediction_id}", response_model=PredictionCalibrationRecordDTO)
async def get_prediction(prediction_id: str):
    """Retrieves an immutable prediction record."""
    pred = _calibration_engine.get_prediction(prediction_id)
    if not pred:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found.")
    return pred


@router.get("/campaigns/{campaign_id}/forecast", response_model=CampaignForecastDTO)
async def get_campaign_forecast(
    campaign_id: str,
    growth_rate: float = Query(1.2, ge=0.0),
    entity_count: int = Query(5, ge=1),
):
    """Retrieves forward-looking campaign expansion forecast."""
    fcst = _forecast_engine.get_campaign_forecast(campaign_id)
    if not fcst:
        fcst = _forecast_engine.forecast_campaign(
            campaign_id=campaign_id,
            entity_count=entity_count,
            daily_growth_rate=growth_rate,
        )
    return fcst


# ---------------------------------------------------------------------------
# Anomalies & Threat Hunting
# ---------------------------------------------------------------------------

@router.get("/anomalies", response_model=List[ThreatAnomalyDTO])
async def list_threat_anomalies(tenant_id: str = Query("default_tenant")):
    """Lists statistical anomalies detected across threat modalities."""
    return _anomaly_engine.list_anomalies(tenant_id)


@router.post("/hunts", response_model=ThreatHuntResultDTO)
async def execute_threat_hunt(query: ThreatHuntQueryDTO):
    """Executes a structured or natural-language threat hunt within tenant isolation boundaries."""
    return _hunt_engine.execute_hunt(query)


@router.get("/hunts/{hunt_id}", response_model=ThreatHuntResultDTO)
async def get_hunt_result(
    hunt_id: str,
    tenant_id: str = Query("default_tenant"),
):
    """Retrieves historical threat hunt results."""
    res = _hunt_engine.get_hunt_result(hunt_id, tenant_id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hunt not found.")
    return res
