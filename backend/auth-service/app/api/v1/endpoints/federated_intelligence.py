"""
TruthShield X — Phase 10 Federated Digital Trust Graph & Threat Intelligence Exchange Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.federation_models import (
    FederatedIntelligenceObjectDTO,
    IntelligenceTypeLiteral,
    SharingScopeLiteral,
    SharingPolicyDecisionDTO,
    IntelligenceConflictDTO,
    IntelligenceSourceReputationDTO,
    IntelligenceQuarantineEntryDTO,
    IntelligenceFeedbackDTO,
)
from app.services.federation.federated_intelligence_service import FederatedIntelligenceService
from app.services.federation.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine
from app.services.federation.intelligence_conflict_engine import IntelligenceConflictEngine
from app.services.federation.source_reputation_engine import SourceReputationEngine
from app.services.federation.intelligence_quarantine_engine import IntelligenceQuarantineEngine
from app.services.federation.cross_tenant_intelligence_safety import CrossTenantIntelligenceSafety


router = APIRouter(prefix="/federated-intelligence", tags=["Federated Digital Trust Graph & Intelligence Exchange"])


_service = FederatedIntelligenceService()
_policy_engine = IntelligenceSharingPolicyEngine()
_conflict_engine = IntelligenceConflictEngine()
_source_engine = SourceReputationEngine()
_quarantine_engine = IntelligenceQuarantineEngine()
_safety_engine = CrossTenantIntelligenceSafety()


class SubmitIntelligenceRequest(BaseModel):
    intelligence_type: IntelligenceTypeLiteral
    canonical_identifier: str
    tenant_scope: str = "default_tenant"
    sharing_scope: SharingScopeLiteral = "PRIVATE"
    classification: str = "CONFIDENTIAL"
    confidence: float = 0.85
    provenance: Optional[Dict[str, Any]] = None
    ttl_days: Optional[int] = 30


class RevokeIntelligenceRequest(BaseModel):
    reason: str
    authorized_by: str


class FeedbackSubmissionRequest(BaseModel):
    feedback_type: str
    notes: Optional[str] = None


@router.post("/submit", response_model=FederatedIntelligenceObjectDTO, status_code=status.HTTP_201_CREATED)
def submit_intelligence(payload: SubmitIntelligenceRequest) -> FederatedIntelligenceObjectDTO:
    """Submits threat intelligence with automatic policy verification."""
    # Policy evaluation if sharing requested
    if payload.sharing_scope != "PRIVATE":
        decision = _policy_engine.evaluate_sharing(
            payload_data={"identifier": payload.canonical_identifier, "prov": payload.provenance},
            requested_scope=payload.sharing_scope,
            data_classification=payload.classification,
        )
        if decision.decision == "REJECT":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=decision.reason)

    return _service.submit_intelligence(
        intelligence_type=payload.intelligence_type,
        canonical_identifier=payload.canonical_identifier,
        tenant_scope=payload.tenant_scope,
        sharing_scope=payload.sharing_scope,
        classification=payload.classification,
        confidence=payload.confidence,
        provenance=payload.provenance,
        ttl_days=payload.ttl_days,
    )


@router.get("/exchange", response_model=List[FederatedIntelligenceObjectDTO])
def list_exchange_intelligence(
    tenant_id: str = "default_tenant",
    intelligence_type: Optional[IntelligenceTypeLiteral] = None,
    scope: Optional[SharingScopeLiteral] = None,
) -> List[FederatedIntelligenceObjectDTO]:
    """Lists federated intelligence objects accessible to tenant."""
    return _service.list_intelligence(requesting_tenant_id=tenant_id, intelligence_type=intelligence_type, scope=scope)


@router.get("/sources", response_model=List[IntelligenceSourceReputationDTO])
def list_feed_sources() -> List[IntelligenceSourceReputationDTO]:
    """Lists all registered threat feed sources and reputation metrics."""
    return _source_engine.list_sources()


@router.get("/conflicts", response_model=List[IntelligenceConflictDTO])
def list_intelligence_conflicts() -> List[IntelligenceConflictDTO]:
    """Lists contradictory intelligence claims requiring resolution."""
    return _conflict_engine.list_conflicts()


@router.get("/quarantine", response_model=List[IntelligenceQuarantineEntryDTO])
def list_quarantined_intelligence() -> List[IntelligenceQuarantineEntryDTO]:
    """Lists threat feeds and indicators isolated under quarantine."""
    return _quarantine_engine.list_quarantine()


@router.get("/{intelligence_id}")
def get_intelligence(
    intelligence_id: str,
    tenant_id: str = "default_tenant",
) -> Dict[str, Any]:
    """Retrieves an intelligence object enforcing cross-tenant privacy sanitization."""
    obj = _service.get_intelligence(intelligence_id, requesting_tenant_id=tenant_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intelligence not found or access denied.")
    return _safety_engine.sanitize_for_consumer(obj, consumer_tenant_id=tenant_id)


@router.post("/{intelligence_id}/revoke", response_model=FederatedIntelligenceObjectDTO)
def revoke_intelligence(
    intelligence_id: str,
    payload: RevokeIntelligenceRequest,
    tenant_id: str = "default_tenant",
) -> FederatedIntelligenceObjectDTO:
    """Revokes incorrect threat intelligence while maintaining historical forensic records."""
    try:
        return _service.revoke_intelligence(
            intelligence_id=intelligence_id,
            revocation_reason=payload.reason,
            authorized_by=payload.authorized_by,
            requesting_tenant_id=tenant_id,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intelligence not found.")
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
