"""FastAPI Endpoints for Enterprise Governance, RBAC/ABAC, Compliance & Audit (Phase 4.0 Part 8 — Sections 86-91)."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.governance_models import (
    OrganizationDTO,
    UserLifecycleDTO,
    RoleDTO,
    GovernancePolicyDTO,
    PolicySimulationDTO,
    LegalHoldDTO,
    PrivacyRequestDTO,
    DataExportManifestDTO,
    AuditEventDTO,
    ComplianceAssessmentDTO,
    ComplianceReportDTO,
    APIKeyMetadataDTO,
    APIKeyCreationResponseDTO,
    GovernancePostureDTO,
)
from app.services.governance_engine import GovernanceEngine

router = APIRouter(prefix="/governance", tags=["Enterprise Governance & Authorization Control Plane"])

# Global governance engine instance
gov_engine = GovernanceEngine()


# Request Payloads
class OrganizationUpdateRequest(BaseModel):
    organization_name: Optional[str] = None
    timezone: Optional[str] = None
    data_residency: Optional[str] = None


class UserInviteRequest(BaseModel):
    email: str
    roles: List[str]
    full_name: str = ""


class RoleCreateRequest(BaseModel):
    name: str
    permissions: List[str]
    description: str = ""
    scope: str = "ORGANIZATION"


class PolicyCreateRequest(BaseModel):
    name: str
    policy_type: str = "ACCESS_CONTROL"
    rules: List[Dict[str, Any]]
    priority: int = 100


class LegalHoldCreateRequest(BaseModel):
    resource_type: str
    resource_id: str
    reason: str


class PrivacyRequestCreate(BaseModel):
    data_principal_id: str
    request_type: str = "ACCESS"
    reason: str = ""


class ExportCreateRequest(BaseModel):
    scope: str = "CASE"
    resource_data: List[Dict[str, Any]] = []
    classification: str = "CONFIDENTIAL"


class APIKeyCreateRequest(BaseModel):
    name: str
    permissions: List[str]
    validity_days: int = 90


# ============================================================================
# Organization Endpoints (Section 86)
# ============================================================================

@router.get("/organization", response_model=Dict[str, Any])
async def get_organization(current_user: User = Depends(get_current_user)):
    org = gov_engine._organizations.get(current_user.organization_id or "org_default")
    if not org:
        org = gov_engine.register_organization("Enterprise Default Org", "default-org")
    return {"success": True, "message": "Organization profile retrieved", "data": org}


# ============================================================================
# User Administration Endpoints (Section 86)
# ============================================================================

@router.get("/users", response_model=Dict[str, Any])
async def list_users(current_user: User = Depends(get_current_user)):
    users = list(gov_engine._users.values())
    return {"success": True, "message": "Organization users retrieved", "data": users}


@router.post("/users/invite", response_model=Dict[str, Any])
async def invite_user(payload: UserInviteRequest, current_user: User = Depends(get_current_user)):
    user = gov_engine.register_user(
        organization_id=current_user.organization_id or "org_default",
        email=payload.email,
        roles=payload.roles,
    )
    user.full_name = payload.full_name
    return {"success": True, "message": "User invited successfully", "data": user}


# ============================================================================
# Roles Endpoints (Section 86)
# ============================================================================

@router.get("/roles", response_model=Dict[str, Any])
async def list_roles(current_user: User = Depends(get_current_user)):
    roles = gov_engine.rbac_engine.list_roles()
    return {"success": True, "message": "Roles retrieved", "data": roles}


@router.post("/roles", response_model=Dict[str, Any])
async def create_role(payload: RoleCreateRequest, current_user: User = Depends(get_current_user)):
    role, ver = gov_engine.rbac_engine.create_or_update_role(
        name=payload.name,
        permissions=payload.permissions,
        organization_id=current_user.organization_id,
        description=payload.description,
        created_by=current_user.email,
    )
    return {"success": True, "message": "Role created and published", "data": {"role": role, "version": ver}}


# ============================================================================
# Policies Endpoints (Section 86)
# ============================================================================

@router.get("/policies", response_model=Dict[str, Any])
async def list_policies(current_user: User = Depends(get_current_user)):
    policies = gov_engine.policy_engine.list_policies(current_user.organization_id)
    return {"success": True, "message": "Governance policies retrieved", "data": policies}


@router.post("/policies", response_model=Dict[str, Any])
async def create_policy(payload: PolicyCreateRequest, current_user: User = Depends(get_current_user)):
    import uuid
    pol_id = f"pol_{uuid.uuid4().hex[:12]}"
    pol, ver = gov_engine.policy_engine.publish_policy(
        policy_id=pol_id,
        organization_id=current_user.organization_id or "org_default",
        name=payload.name,
        policy_type=payload.policy_type,
        rules=payload.rules,
        created_by=current_user.email,
        priority=payload.priority,
    )
    return {"success": True, "message": "Policy published", "data": {"policy": pol, "version": ver}}


@router.post("/policies/{policy_id}/simulate", response_model=Dict[str, Any])
async def simulate_policy(policy_id: str, current_user: User = Depends(get_current_user)):
    pol = gov_engine.policy_engine.get_policy(policy_id)
    if not pol:
        raise HTTPException(status_code=404, detail="Policy not found")
    sim = gov_engine.simulation_engine.simulate_policy(pol)
    return {"success": True, "message": "Policy simulation completed with zero mutations", "data": sim}


# ============================================================================
# Audit Endpoints (Section 87)
# ============================================================================

@router.get("/audit", response_model=Dict[str, Any])
async def query_audit(
    actor_id: Optional[str] = None,
    action: Optional[str] = None,
    result: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
):
    events = gov_engine.audit_service.query_audit_events(
        organization_id=current_user.organization_id,
        actor_id=actor_id,
        action=action,
        result=result,
        limit=limit,
    )
    return {"success": True, "message": "Audit events retrieved", "data": events}


@router.get("/audit/integrity", response_model=Dict[str, Any])
async def verify_audit_integrity(current_user: User = Depends(get_current_user)):
    is_valid = gov_engine.audit_service.verify_integrity()
    return {"success": True, "message": "Audit hash chain verified", "data": {"integrity_status": "VERIFIED" if is_valid else "CORRUPTED"}}


# ============================================================================
# Compliance Endpoints (Section 88)
# ============================================================================

@router.get("/compliance/frameworks", response_model=Dict[str, Any])
async def list_frameworks(current_user: User = Depends(get_current_user)):
    fws = gov_engine.compliance_engine.list_frameworks()
    return {"success": True, "message": "Compliance frameworks retrieved", "data": fws}


@router.post("/compliance/{framework_id}/assess", response_model=Dict[str, Any])
async def assess_framework(framework_id: str, current_user: User = Depends(get_current_user)):
    ass = gov_engine.compliance_engine.assess_framework(framework_id, current_user.organization_id or "org_default")
    return {"success": True, "message": "Compliance assessment completed", "data": ass}


@router.get("/compliance/{framework_id}/report", response_model=Dict[str, Any])
async def get_compliance_report(framework_id: str, current_user: User = Depends(get_current_user)):
    rep = gov_engine.compliance_engine.generate_compliance_report(framework_id, current_user.organization_id or "org_default")
    return {"success": True, "message": "Compliance report generated", "data": rep}


# ============================================================================
# Retention & Legal Hold Endpoints (Section 89)
# ============================================================================

@router.get("/legal-holds", response_model=Dict[str, Any])
async def list_legal_holds(current_user: User = Depends(get_current_user)):
    holds = gov_engine.legal_hold_engine.list_holds(current_user.organization_id)
    return {"success": True, "message": "Legal holds retrieved", "data": holds}


@router.post("/legal-holds", response_model=Dict[str, Any])
async def create_legal_hold(payload: LegalHoldCreateRequest, current_user: User = Depends(get_current_user)):
    hold = gov_engine.legal_hold_engine.apply_legal_hold(
        organization_id=current_user.organization_id or "org_default",
        resource_type=payload.resource_type,
        resource_id=payload.resource_id,
        reason=payload.reason,
        created_by=current_user.email,
    )
    return {"success": True, "message": "Legal hold established", "data": hold}


# ============================================================================
# Privacy & Data Export Endpoints (Section 89)
# ============================================================================

@router.post("/privacy-requests", response_model=Dict[str, Any])
async def submit_privacy_request(payload: PrivacyRequestCreate, current_user: User = Depends(get_current_user)):
    req = gov_engine.privacy_engine.submit_privacy_request(
        organization_id=current_user.organization_id or "org_default",
        data_principal_id=payload.data_principal_id,
        request_type=payload.request_type,
        reason=payload.reason,
    )
    return {"success": True, "message": "Privacy request logged", "data": req}


@router.post("/exports", response_model=Dict[str, Any])
async def create_export(payload: ExportCreateRequest, current_user: User = Depends(get_current_user)):
    try:
        manifest = gov_engine.export_engine.create_data_export(
            organization_id=current_user.organization_id or "org_default",
            requester_id=current_user.email,
            requester_roles=current_user.roles if hasattr(current_user, "roles") else ["ORG_ADMIN"],
            scope=payload.scope,
            resource_data=payload.resource_data,
            classification=payload.classification,
        )
        return {"success": True, "message": "Export manifest generated", "data": manifest}
    except Exception as ex:
        raise HTTPException(status_code=403, detail=str(ex))


# ============================================================================
# API Key Endpoints (Section 91)
# ============================================================================

@router.get("/api-keys", response_model=Dict[str, Any])
async def list_api_keys(current_user: User = Depends(get_current_user)):
    keys = gov_engine.api_key_service.list_api_keys(current_user.organization_id)
    return {"success": True, "message": "API keys metadata retrieved", "data": keys}


@router.post("/api-keys", response_model=Dict[str, Any])
async def create_api_key(payload: APIKeyCreateRequest, current_user: User = Depends(get_current_user)):
    resp, meta = gov_engine.api_key_service.create_api_key(
        organization_id=current_user.organization_id or "org_default",
        name=payload.name,
        owner_id=current_user.email,
        permissions=payload.permissions,
        validity_days=payload.validity_days,
    )
    return {"success": True, "message": "API key generated. Store the raw secret safely; it will not be shown again.", "data": resp}


@router.post("/api-keys/{key_id}/revoke", response_model=Dict[str, Any])
async def revoke_api_key(key_id: str, current_user: User = Depends(get_current_user)):
    key = gov_engine.api_key_service.revoke_api_key(key_id)
    return {"success": True, "message": "API key revoked", "data": key}
