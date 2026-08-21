"""
TruthShield X — Phase 33 Threat Intelligence Fusion FastAPI Router.
"""

from typing import Dict, List, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from app.services.threat_intelligence_fusion.threat_intelligence_fusion_engine import ThreatIntelligenceFusionEngine

router = APIRouter(prefix="/threat-intelligence-fusion", tags=["Threat Intelligence Fusion"])

_fusion_engine = ThreatIntelligenceFusionEngine()


class QuarantineRequest(BaseModel):
    reason: str


class DisseminateRequest(BaseModel):
    product_type: str
    recipient: str
    classification: str
    requester_clearance: str
    tenant_scope: str = "GLOBAL"
    recipient_tenant: str = "GLOBAL"


class ThreatContentCheckRequest(BaseModel):
    raw_content: str


@router.get("/overview")
def get_fusion_overview():
    return _fusion_engine.get_overview()


@router.get("/sources")
def list_sources(approval_status: Optional[str] = None):
    return _fusion_engine.sources.list_sources(approval_status=approval_status)


@router.get("/indicators")
def list_indicators(status: Optional[str] = None):
    return _fusion_engine.indicators.list_indicators(status=status)


@router.get("/campaigns")
def list_campaigns(status: Optional[str] = None):
    return _fusion_engine.campaigns.list_campaigns(status=status)


@router.get("/actors")
def list_actors(attribution_status: Optional[str] = None):
    return _fusion_engine.actors.list_actors(attribution_status=attribution_status)


@router.get("/malware")
def list_malware():
    return _fusion_engine.malware.list_malware()


@router.get("/vulnerabilities")
def list_vulnerabilities(exploitation_status: Optional[str] = None):
    return _fusion_engine.vulnerabilities.list_vulnerabilities(exploitation_status=exploitation_status)


@router.get("/graph")
def query_graph(entity_id: Optional[str] = None):
    return _fusion_engine.graph.query_graph(entity_id=entity_id)


@router.get("/forecasts")
def list_forecasts():
    return _fusion_engine.forecasting.list_forecasts()


@router.get("/early-warning")
def list_early_warnings(urgency: Optional[str] = None):
    return _fusion_engine.early_warning.list_warnings(urgency=urgency)


@router.get("/conflicts")
def list_conflicts():
    return _fusion_engine.corroboration.list_conflicts()


@router.get("/snapshots")
def list_snapshots():
    return _fusion_engine.graph.list_snapshots()


@router.post("/feeds/{source_id}/quarantine")
def quarantine_feed(source_id: str, req: QuarantineRequest):
    res = _fusion_engine.sources.quarantine_source(source_id, req.reason)
    if res.get("status") == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Source not found")
    return res


@router.post("/disseminate")
def evaluate_dissemination(req: DisseminateRequest):
    return _fusion_engine.dissemination.evaluate_dissemination_policy(
        product_type=req.product_type,
        recipient=req.recipient,
        classification=req.classification,
        requester_clearance=req.requester_clearance,
        tenant_scope=req.tenant_scope,
        recipient_tenant=req.recipient_tenant,
    )


@router.post("/detect-injection")
def detect_content_injection(req: ThreatContentCheckRequest):
    return _fusion_engine.dissemination.sanitize_untrusted_threat_content(req.raw_content)
