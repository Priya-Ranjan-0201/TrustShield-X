"""
TruthShield X — Threat Intelligence Fabric API Endpoints (Phase 22).

REST API for querying threat intelligence sources, objects, graphs, campaigns, local relevance,
early warnings, forecasts, quality metrics, and collaborative defense sharing/disputes.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel

from app.schemas.threat_intelligence_fabric_models import (
    IntelligenceSourceDTO,
    FeedHealthDTO,
    ThreatIntelligenceObjectDTO,
    ThreatIntelligenceGraphDTO,
    CampaignClusterDTO,
    LocalThreatRelevanceDTO,
    ThreatEarlyWarningDTO,
    ThreatForecastDTO,
    CollaborativeContributionDTO,
    IntelligenceDisputeDTO,
    IntelligenceRevocationDTO,
    IntelligenceQualityMetricsDTO,
)
from app.services.threat_intelligence.threat_intelligence_fabric import ThreatIntelligenceFabric

router = APIRouter(prefix="/intelligence", tags=["Threat Intelligence Fabric (Phase 22)"])

_fabric_instance = ThreatIntelligenceFabric()


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class IngestIntelligenceRequest(BaseModel):
    raw_data: Dict[str, Any]
    source_id: str
    tenant_id: str = "default_tenant"
    feed_format: str = "STIX2"


class ContributeIntelligenceRequest(BaseModel):
    tenant_id: str = "default_tenant"
    contributor: str = "usr_soc_analyst"
    raw_intelligence: str
    classification: str = "COMMUNITY"


class DisputeIntelligenceRequest(BaseModel):
    object_id: str
    tenant_id: str = "default_tenant"
    reason: str


class RevokeIntelligenceRequest(BaseModel):
    object_id: str
    reason: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/sources", response_model=List[IntelligenceSourceDTO])
def list_intelligence_sources(tenant_id: str = "default_tenant"):
    return _fabric_instance.sources.list_sources(tenant_id)


@router.get("/feed-health", response_model=FeedHealthDTO)
def get_feed_health(feed_id: str = "src_crowdstrike_falcon"):
    return _fabric_instance.feed_health.get_feed_health(feed_id)


@router.get("/search", response_model=List[ThreatIntelligenceObjectDTO])
def search_intelligence(query: str = Query(..., description="Indicator or threat query"), tenant_id: str = "default_tenant"):
    return _fabric_instance.search_intelligence(query, tenant_id)


@router.get("/campaigns", response_model=List[CampaignClusterDTO])
def list_campaigns():
    return _fabric_instance.campaigns.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=CampaignClusterDTO)
def get_campaign(campaign_id: str):
    camp = _fabric_instance.campaigns.get_campaign(campaign_id)
    if not camp:
        raise HTTPException(status_code=404, detail=f"Campaign '{campaign_id}' not found.")
    return camp


@router.get("/graph", response_model=ThreatIntelligenceGraphDTO)
def get_threat_graph(start_node_id: str = "node_camp_shadow", depth: int = 3):
    return _fabric_instance.graph.get_subgraph(start_node_id, max_depth=depth)


@router.get("/relevance", response_model=LocalThreatRelevanceDTO)
def get_local_threat_relevance(tenant_id: str = "default_tenant", threat_id: str = "camp_shadowstrike"):
    return _fabric_instance.relevance.compute_relevance(
        tenant_id=tenant_id,
        threat_entity_id=threat_id,
        targeted_technologies=["NGINX", "POSTGRES", "DOCKER"],
        tenant_inventory_techs=["NGINX", "KUBERNETES", "REACT"],
        exposed_assets=["srv_checkout_pod_3"],
    )


@router.get("/early-warning", response_model=List[ThreatEarlyWarningDTO])
@router.get("/early-warnings", response_model=List[ThreatEarlyWarningDTO])
def get_early_warnings():
    return _fabric_instance.early_warning.list_early_warnings()


@router.get("/forecasts", response_model=List[ThreatForecastDTO])
def get_threat_forecasts():
    return _fabric_instance.forecast.list_forecasts()


@router.get("/quality", response_model=IntelligenceQualityMetricsDTO)
@router.get("/quality-metrics", response_model=IntelligenceQualityMetricsDTO)
def get_intelligence_quality():
    return _fabric_instance.quality.compute_quality_metrics()



@router.get("/{object_id}", response_model=ThreatIntelligenceObjectDTO)
def get_intelligence_object(object_id: str):
    obj = _fabric_instance.get_object(object_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Threat object '{object_id}' not found.")
    return obj


@router.post("/ingest")
def ingest_intelligence(req: IngestIntelligenceRequest):
    return _fabric_instance.ingest_raw_intelligence(
        raw_data=req.raw_data,
        source_id=req.source_id,
        tenant_id=req.tenant_id,
        feed_format=req.feed_format,
    )


@router.post("/contribute", response_model=CollaborativeContributionDTO)
def contribute_intelligence(req: ContributeIntelligenceRequest):
    return _fabric_instance.collaboration.contribute_intelligence(
        tenant_id=req.tenant_id,
        contributor=req.contributor,
        raw_intelligence=req.raw_intelligence,
        classification=req.classification,  # type: ignore
    )


@router.post("/dispute", response_model=IntelligenceDisputeDTO)
def dispute_intelligence(req: DisputeIntelligenceRequest):
    return _fabric_instance.collaboration.submit_dispute(
        object_id=req.object_id,
        tenant_id=req.tenant_id,
        reason=req.reason,
    )


@router.post("/revoke", response_model=IntelligenceRevocationDTO)
def revoke_intelligence(req: RevokeIntelligenceRequest):
    return _fabric_instance.collaboration.revoke_intelligence(
        object_id=req.object_id,
        reason=req.reason,
    )
