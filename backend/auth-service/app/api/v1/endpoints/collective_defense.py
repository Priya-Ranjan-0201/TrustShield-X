"""
TruthShield X — Phase 16 Collective Defense & Global Threat Intelligence Endpoints.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    CollectiveDefenseCenterSummaryDTO,
    GlobalCampaignDetailDTO,
    GlobalCampaignGraphDTO,
    GlobalEarlyWarningDTO,
    FederationPartnerDTO,
    IntelligenceDisputeDTO,
    IntelligenceQualityScoreDTO,
    RevocationImpactAssessmentDTO,
)
from app.services.collective_defense.collective_defense_fabric import CollectiveDefenseFabric

router = APIRouter(prefix="/collective-defense", tags=["Collective Defense & Global Threat Intelligence"])

_fabric = CollectiveDefenseFabric()


class SubmitIntelligenceRequest(BaseModel):
    intelligence_type: str = "DOMAIN"
    raw_indicator: str
    tenant_id: str = "default_tenant"
    tenant_industry: str = "FINANCIAL_SERVICES"
    classification: str = "INTERNAL"
    confidence: float = 0.80
    tags: List[str] = []


class RegisterPartnerRequest(BaseModel):
    name: str
    trust_level: float = 0.80
    scopes: List[str] = ["threat_indicators"]
    auth_key: str = "partner_secret_123"
    rate_limit: int = 100


class SubmitDisputeRequest(BaseModel):
    intelligence_id: str
    tenant_id: str = "default_tenant"
    dispute_type: str = "FALSE_POSITIVE"
    reason: str
    evidence: str = ""


class ResolveDisputeRequest(BaseModel):
    resolution: str
    status: str = "RESOLVED"
    reviewer_notes: Optional[str] = None


class RevokeIndicatorRequest(BaseModel):
    reason: str
    revoked_by: str = "SOC_LEAD"


@router.get("/summary", response_model=CollectiveDefenseCenterSummaryDTO)
def get_collective_defense_summary() -> CollectiveDefenseCenterSummaryDTO:
    """Returns aggregated collective defense statistics."""
    return _fabric.get_summary()


@router.get("/feed", response_model=List[ThreatIntelligenceObjectDTO])
def get_threat_feed() -> List[ThreatIntelligenceObjectDTO]:
    """Returns privacy-safe shared collective threat intelligence feed."""
    return _fabric.normalization.list_all()


@router.post("/submit", response_model=ThreatIntelligenceObjectDTO)
def submit_intelligence(payload: SubmitIntelligenceRequest) -> ThreatIntelligenceObjectDTO:
    """Submits local intelligence with policy validation and privacy transformation."""
    obj = ThreatIntelligenceObjectDTO(
        intelligence_type=payload.intelligence_type,  # type: ignore
        raw_indicator=payload.raw_indicator,
        tenant_id=payload.tenant_id,
        classification=payload.classification,  # type: ignore
        confidence=payload.confidence,
        tags=payload.tags,
    )
    result = _fabric.process_and_share_local_intelligence(obj, payload.tenant_industry)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sharing blocked by policy or sensitive data detected.",
        )
    return result


@router.get("/campaigns", response_model=List[GlobalCampaignDetailDTO])
def list_global_campaigns() -> List[GlobalCampaignDetailDTO]:
    """Lists global correlated threat campaigns."""
    return _fabric.campaign_graph.list_campaigns()


@router.get("/campaigns/{campaign_id}", response_model=GlobalCampaignDetailDTO)
def get_global_campaign(campaign_id: str) -> GlobalCampaignDetailDTO:
    """Returns details for a specific global campaign."""
    cmp = _fabric.campaign_graph.get_campaign(campaign_id)
    if not cmp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found.")
    return cmp


@router.get("/early-warning", response_model=List[GlobalEarlyWarningDTO])
def list_early_warnings() -> List[GlobalEarlyWarningDTO]:
    """Returns active global early warnings."""
    return _fabric.early_warning.list_warnings()


@router.get("/graph", response_model=GlobalCampaignGraphDTO)
def export_campaign_graph() -> GlobalCampaignGraphDTO:
    """Exports privacy-preserving global campaign knowledge graph."""
    return _fabric.campaign_graph.export_graph()


@router.get("/partners", response_model=List[FederationPartnerDTO])
def list_federation_partners() -> List[FederationPartnerDTO]:
    """Lists registered federation exchange partners."""
    return _fabric.partner_registry.list_partners()


@router.post("/partners", response_model=FederationPartnerDTO)
def register_federation_partner(payload: RegisterPartnerRequest) -> FederationPartnerDTO:
    """Registers a new federation exchange partner."""
    return _fabric.partner_registry.register_partner(
        name=payload.name,
        trust_level=payload.trust_level,
        scopes=payload.scopes,
        auth_key=payload.auth_key,
        rate_limit=payload.rate_limit,
    )


@router.get("/disputes", response_model=List[IntelligenceDisputeDTO])
def list_disputes() -> List[IntelligenceDisputeDTO]:
    """Lists all intelligence disputes."""
    return _fabric.dispute.list_all_disputes()


@router.post("/disputes", response_model=IntelligenceDisputeDTO)
def submit_dispute(payload: SubmitDisputeRequest) -> IntelligenceDisputeDTO:
    """Submits a dispute against an intelligence indicator."""
    return _fabric.dispute.submit_dispute(
        intelligence_id=payload.intelligence_id,
        tenant_id=payload.tenant_id,
        dispute_type=payload.dispute_type,
        reason=payload.reason,
        evidence=payload.evidence,
    )


@router.post("/disputes/{dispute_id}/resolve", response_model=IntelligenceDisputeDTO)
def resolve_dispute(dispute_id: str, payload: ResolveDisputeRequest) -> IntelligenceDisputeDTO:
    """Resolves an indicator dispute."""
    res = _fabric.dispute.resolve_dispute(
        dispute_id=dispute_id,
        resolution=payload.resolution,
        status=payload.status,  # type: ignore
        reviewer_notes=payload.reviewer_notes,
    )
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispute not found.")
    return res


@router.post("/revoke/{intelligence_id}", response_model=RevocationImpactAssessmentDTO)
def revoke_indicator(intelligence_id: str, payload: RevokeIndicatorRequest) -> RevocationImpactAssessmentDTO:
    """Revokes an indicator and calculates downstream impact."""
    objs = [o for o in _fabric.normalization.list_all() if o.intelligence_id == intelligence_id]
    if not objs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Indicator not found.")
    return _fabric.revocation.revoke_intelligence(objs[0], payload.reason, payload.revoked_by)


@router.get("/search", response_model=List[ThreatIntelligenceObjectDTO])
def search_intelligence(
    q: str,
    tenant_id: str = "default_tenant",
) -> List[ThreatIntelligenceObjectDTO]:
    """Searches intelligence objects with classification and tenant filtering."""
    return _fabric.search_intelligence(q, tenant_id)
