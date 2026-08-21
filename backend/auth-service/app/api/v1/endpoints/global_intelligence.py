"""
TruthShield X — Global Threat Intelligence REST API (Phase 27).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.global_intelligence_models import (
    IntelligenceSourceDTO,
    ThreatIntelligenceRecordDTO,
    ThreatCampaignDTO,
    ThreatForecastDTO,
    EarlyWarningSignalDTO,
    DefensiveHypothesisDTO,
)
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

router = APIRouter(prefix="/global-intelligence", tags=["Global Threat Intelligence Fusion & Predictive Forecasting"])

# Singleton engine instance
global_intel_engine = GlobalThreatIntelligenceFusionEngine()


# ============================================================================
# Overview & Sources
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_global_intelligence_overview(tenant_scope: str = Query("default_tenant")):
    return global_intel_engine.get_global_intelligence_overview(tenant_scope)


@router.get("/sources", response_model=List[IntelligenceSourceDTO])
def list_sources(tenant_scope: str = Query("default_tenant")):
    return global_intel_engine.source_manager.list_sources(tenant_scope)


class IngestRecordRequest(BaseModel):
    source_id: str
    raw_payload: Dict[str, Any]
    tenant_scope: str = "default_tenant"


@router.post("/ingest", response_model=ThreatIntelligenceRecordDTO)
def ingest_intelligence_record(payload: IngestRecordRequest):
    return global_intel_engine.ingest_record(
        source_id=payload.source_id,
        raw_payload=payload.raw_payload,
        tenant_scope=payload.tenant_scope,
    )


@router.get("/records", response_model=List[ThreatIntelligenceRecordDTO])
def list_intelligence_records():
    return global_intel_engine.list_records()


# ============================================================================
# Campaigns & Graph
# ============================================================================

@router.get("/campaigns", response_model=List[ThreatCampaignDTO])
def list_threat_campaigns():
    return global_intel_engine.campaign_engine.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=ThreatCampaignDTO)
def get_threat_campaign(campaign_id: str):
    cmp_obj = global_intel_engine.campaign_engine.get_campaign(campaign_id)
    if not cmp_obj:
        raise HTTPException(status_code=404, detail="Threat campaign not found")
    return cmp_obj


@router.get("/graph", response_model=List[Dict[str, Any]])
def query_threat_graph(entity_id: str = Query("node_darkstorm_c2")):
    return global_intel_engine.temporal_graph_engine.query_temporal_relationships(entity_id)


# ============================================================================
# Predictive Forecasts & Early Warnings
# ============================================================================

@router.get("/forecasts", response_model=List[ThreatForecastDTO])
def list_threat_forecasts():
    return global_intel_engine.forecasting_engine.list_forecasts()


class CreateForecastRequest(BaseModel):
    subject: str
    horizon: str = "SHORT_TERM"
    prediction: str
    evidence: List[str]
    confidence_score: float = 0.85
    methodology: str = "Empirical Trend Regression"


@router.post("/forecasts", response_model=ThreatForecastDTO)
def create_threat_forecast(payload: CreateForecastRequest):
    return global_intel_engine.forecasting_engine.generate_forecast(
        subject=payload.subject,
        horizon=payload.horizon,  # type: ignore
        prediction=payload.prediction,
        evidence=payload.evidence,
        confidence_score=payload.confidence_score,
        methodology=payload.methodology,
    )


@router.get("/forecasts/{forecast_id}", response_model=ThreatForecastDTO)
def get_threat_forecast(forecast_id: str):
    fcst = global_intel_engine.forecasting_engine.get_forecast(forecast_id)
    if not fcst:
        raise HTTPException(status_code=404, detail="Threat forecast not found")
    return fcst


@router.get("/early-warning", response_model=List[EarlyWarningSignalDTO])
def list_early_warnings():
    return global_intel_engine.early_warning_engine.list_warnings()


# ============================================================================
# Watchlists, Calibration & Feed Health
# ============================================================================

@router.get("/watchlists", response_model=List[Dict[str, Any]])
def list_watchlists():
    return global_intel_engine.list_watchlists()


class CreateWatchlistRequest(BaseModel):
    category: str
    target: str


@router.post("/watchlists", response_model=Dict[str, Any])
def add_watchlist(payload: CreateWatchlistRequest):
    return global_intel_engine.add_watchlist(category=payload.category, target=payload.target)


@router.get("/calibration", response_model=List[Dict[str, Any]])
def list_forecast_calibrations():
    return global_intel_engine.calibration_engine.list_calibrations()


@router.get("/feed-health", response_model=Dict[str, Any])
def get_feed_health(source_id: str = Query("src_global_exchange")):
    return global_intel_engine.source_manager.get_feed_health(source_id)
