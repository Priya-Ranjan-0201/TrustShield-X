"""
TruthShield X — Enterprise Security & Compliance REST API (Phase 32).
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.schemas.enterprise_governance_models import (
    ControlDTO,
    ComplianceRequirementDTO,
    EvidenceDTO,
    EnterpriseRiskDTO,
    ComplianceFindingDTO,
    RemediationTaskDTO,
    SecurityExceptionDTO,
    AuditRequestDTO,
    ThirdPartyRiskDTO,
    ComplianceDriftEventDTO,
)
from app.services.enterprise_governance.enterprise_governance_engine import EnterpriseGovernanceEngine

router = APIRouter(prefix="/compliance", tags=["Enterprise Security & Compliance Operating System"])

# Singleton Engine Instance
enterprise_governance_engine = EnterpriseGovernanceEngine()


# ============================================================================
# Executive Overview & Posture
# ============================================================================

@router.get("/overview", response_model=Dict[str, Any])
def get_executive_compliance_overview(tenant_id: str = Query("default_tenant")):
    return enterprise_governance_engine.get_executive_governance_summary(tenant_id)


@router.get("/compliance-posture", response_model=Dict[str, Any])
def get_compliance_posture():
    return {
        "governance_posture": "EFFECTIVE",
        "access_posture": "EFFECTIVE",
        "data_posture": "EFFECTIVE",
        "security_posture": "EFFECTIVE",
        "privacy_posture": "EFFECTIVE",
        "ai_posture": "EFFECTIVE",
        "resilience_posture": "EFFECTIVE",
        "incident_posture": "EFFECTIVE",
        "third_party_posture": "EFFECTIVE",
        "continuous_assurance": "ACTIVE",
    }


# ============================================================================
# Controls, Requirements & Evidence
# ============================================================================

@router.get("/controls", response_model=List[ControlDTO])
def list_controls(tenant_id: str = Query("default_tenant")):
    return enterprise_governance_engine.control_catalog.list_controls(tenant_id)


@router.get("/controls/{control_id}", response_model=Dict[str, Any])
def get_control(control_id: str):
    ctrl = enterprise_governance_engine.control_catalog.get_control(control_id)
    if not ctrl:
        raise HTTPException(status_code=404, detail="Control not found")
    return {"control": ctrl}


@router.get("/requirements", response_model=List[ComplianceRequirementDTO])
def list_requirements():
    return enterprise_governance_engine.requirement_registry.list_requirements()


@router.get("/evidence", response_model=List[EvidenceDTO])
def list_evidence():
    return enterprise_governance_engine.evidence_engine.list_evidence()


# ============================================================================
# Risks, Findings & Remediation
# ============================================================================

@router.get("/risks", response_model=List[EnterpriseRiskDTO])
def list_enterprise_risks():
    return enterprise_governance_engine.risk_engine.list_risks()


@router.get("/findings", response_model=List[ComplianceFindingDTO])
def list_findings():
    return enterprise_governance_engine.remediation_engine.list_findings()


@router.get("/remediation", response_model=List[RemediationTaskDTO])
def list_remediation_tasks():
    return enterprise_governance_engine.remediation_engine.list_tasks()


# ============================================================================
# Exceptions, Audit Requests, Third-Party & Drift
# ============================================================================

@router.get("/exceptions", response_model=List[SecurityExceptionDTO])
def list_security_exceptions():
    return enterprise_governance_engine.exception_engine.list_exceptions()


@router.get("/audit-requests", response_model=List[AuditRequestDTO])
def list_audit_requests():
    return enterprise_governance_engine.audit_engine.list_requests()


@router.get("/third-party-risk", response_model=List[ThirdPartyRiskDTO])
def list_third_party_vendors():
    return enterprise_governance_engine.third_party_engine.list_vendors()


@router.get("/access-reviews", response_model=Dict[str, Any])
def get_access_reviews(tenant_id: str = Query("default_tenant")):
    return enterprise_governance_engine.access_review_engine.perform_privileged_access_review(tenant_id)


@router.get("/drift", response_model=List[ComplianceDriftEventDTO])
def list_compliance_drift():
    return enterprise_governance_engine.assurance_engine.list_drift_events()
