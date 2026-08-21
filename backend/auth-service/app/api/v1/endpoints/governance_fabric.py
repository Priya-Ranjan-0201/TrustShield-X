"""
TruthShield X — Phase 14 Continuous Security Governance & Compliance Evidence Fabric Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.governance_fabric_models import (
    GovernanceFrameworkDTO,
    GovernanceRequirementDTO,
    ControlMappingDTO,
    GovernanceEvidenceDTO,
    GovernanceExceptionDTO,
    AuditPackageDTO,
    GovernancePostureSummaryDTO,
)
from app.services.governance_fabric.governance_framework_registry import GovernanceFrameworkRegistry
from app.services.governance_fabric.control_mapping_engine import ControlMappingEngine
from app.services.governance_fabric.governance_evidence_collector import GovernanceEvidenceCollector
from app.services.governance_fabric.governance_exception_engine import GovernanceExceptionEngine
from app.services.governance_fabric.audit_preparation_engine import AuditPreparationEngine
from app.services.governance_fabric.governance_posture_engine import GovernancePostureEngine


router = APIRouter(prefix="/governance-fabric", tags=["Continuous Governance, Zero-Trust Assurance & Audit Fabric"])

_frameworks = GovernanceFrameworkRegistry()
_mappings = ControlMappingEngine()
_evidence = GovernanceEvidenceCollector()
_exceptions = GovernanceExceptionEngine()
_audit = AuditPreparationEngine()
_posture = GovernancePostureEngine()


class CreateExceptionRequest(BaseModel):
    requirement_id: str
    control_id: str
    reason: str
    business_justification: str
    owner: str
    approver: str
    duration_days: int = 30
    compensating_control_id: Optional[str] = None


class CompileAuditPackageRequest(BaseModel):
    framework_id: str
    framework_version: str = "2023"


@router.get("", response_model=GovernancePostureSummaryDTO)
def get_governance_posture() -> GovernancePostureSummaryDTO:
    """Returns the consolidated continuous governance posture and compliance confidence."""
    fws = _frameworks.list_frameworks()
    reqs = _frameworks.list_requirements()
    exps = _exceptions.list_exceptions()
    evs = _evidence.list_evidence()
    return _posture.calculate_posture(len(fws), reqs, exps, evs)


@router.get("/frameworks", response_model=List[GovernanceFrameworkDTO])
def list_frameworks() -> List[GovernanceFrameworkDTO]:
    """Lists versioned compliance frameworks (DPDP 2023, ISO 27001, SOC 2, NIST CSF)."""
    return _frameworks.list_frameworks()


@router.get("/requirements", response_model=List[GovernanceRequirementDTO])
def list_requirements(framework_id: Optional[str] = None) -> List[GovernanceRequirementDTO]:
    """Lists verifiable requirements."""
    return _frameworks.list_requirements(framework_id)


@router.get("/requirements/{requirement_id}", response_model=GovernanceRequirementDTO)
def get_requirement(requirement_id: str) -> GovernanceRequirementDTO:
    """Retrieves a single requirement."""
    req = _frameworks.get_requirement(requirement_id)
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found.")
    return req


@router.get("/mappings", response_model=List[ControlMappingDTO])
def list_mappings(requirement_id: Optional[str] = None) -> List[ControlMappingDTO]:
    """Lists traceable requirement-to-control mappings."""
    return _mappings.list_mappings(requirement_id)


@router.get("/evidence", response_model=List[GovernanceEvidenceDTO])
def list_evidence(tenant_id: str = "PLATFORM_SCOPE") -> List[GovernanceEvidenceDTO]:
    """Lists empirical evidence records."""
    return _evidence.list_evidence(tenant_id)


@router.get("/exceptions", response_model=List[GovernanceExceptionDTO])
def list_exceptions() -> List[GovernanceExceptionDTO]:
    """Lists governance exceptions."""
    return _exceptions.list_exceptions()


@router.post("/exceptions", response_model=GovernanceExceptionDTO)
def create_exception(payload: CreateExceptionRequest) -> GovernanceExceptionDTO:
    """Submits a new exception with four-eyes approval validation."""
    try:
        return _exceptions.request_exception(
            requirement_id=payload.requirement_id,
            control_id=payload.control_id,
            reason=payload.reason,
            business_justification=payload.business_justification,
            owner=payload.owner,
            approver=payload.approver,
            duration_days=payload.duration_days,
            compensating_control_id=payload.compensating_control_id,
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/audit-packages", response_model=AuditPackageDTO)
def generate_audit_package(payload: CompileAuditPackageRequest) -> AuditPackageDTO:
    """Generates an audit evidence package with a SHA-256 cryptographic manifest."""
    reqs = _frameworks.list_requirements(payload.framework_id)
    evs = _evidence.list_evidence()
    exps = _exceptions.list_exceptions()
    return _audit.compile_audit_package(
        framework_id=payload.framework_id,
        framework_version=payload.framework_version,
        requirements=reqs,
        evidence_list=evs,
        exceptions_count=len(exps),
    )
