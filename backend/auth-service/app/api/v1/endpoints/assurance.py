"""
TruthShield X — Phase 13 Continuous Security Assurance & Control Certification Endpoints
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from app.schemas.assurance_models import (
    SecurityControlRegistryDTO,
    SecurityAssuranceSummaryDTO,
    SecurityInvariantDTO,
    SecurityDriftDTO,
    SecuritySLODTO,
    ControlTestExecutionDTO,
)
from app.services.assurance.security_control_registry_service import SecurityControlRegistryService
from app.services.assurance.security_invariant_engine import SecurityInvariantEngine
from app.services.assurance.control_testing_framework import ControlTestingFramework
from app.services.assurance.security_drift_engine import SecurityDriftEngine
from app.services.assurance.control_dependency_graph_engine import ControlDependencyGraphEngine
from app.services.assurance.security_slo_engine import SecuritySLOEngine
from app.services.assurance.security_assurance_score_engine import SecurityAssuranceScoreEngine


router = APIRouter(prefix="/assurance", tags=["Continuous Security Control Assurance & Certification"])

_registry = SecurityControlRegistryService()
_invariants = SecurityInvariantEngine()
_testing = ControlTestingFramework()
_drift = SecurityDriftEngine()
_dependencies = ControlDependencyGraphEngine()
_slo = SecuritySLOEngine()
_score_engine = SecurityAssuranceScoreEngine()


class RunTestRequest(BaseModel):
    test_id: str
    control_id: str
    environment: str = "STAGING"
    force_failure: bool = False


@router.get("", response_model=SecurityAssuranceSummaryDTO)
def get_assurance_summary(tenant_id: str = "PLATFORM_SCOPE") -> SecurityAssuranceSummaryDTO:
    """Returns the consolidated continuous security assurance and certification score."""
    controls = _registry.list_controls(tenant_id)
    drifts = _drift.list_drifts()
    return _score_engine.calculate_summary(controls, active_drifts_count=len(drifts))


@router.get("/controls", response_model=List[SecurityControlRegistryDTO])
def list_security_controls(tenant_id: str = "PLATFORM_SCOPE") -> List[SecurityControlRegistryDTO]:
    """Lists all cataloged security controls and their empirical verification states."""
    return _registry.list_controls(tenant_id)


@router.get("/controls/{control_id}", response_model=SecurityControlRegistryDTO)
def get_security_control(control_id: str, tenant_id: str = "PLATFORM_SCOPE") -> SecurityControlRegistryDTO:
    """Retrieves single control metadata and evidence."""
    ctrl = _registry.get_control(control_id, tenant_id)
    if not ctrl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Security control not found.")
    return ctrl


@router.post("/tests/run", response_model=ControlTestExecutionDTO)
def run_control_test(payload: RunTestRequest) -> ControlTestExecutionDTO:
    """Executes a security control test with false-pass prevention."""
    execution = _testing.execute_test(
        test_id=payload.test_id,
        control_id=payload.control_id,
        environment=payload.environment,
        force_failure=payload.force_failure,
    )

    # Update control state
    new_state = "VERIFIED" if execution.result == "PASS" else "FAILED"
    try:
        _registry.update_verification_state(payload.control_id, new_state)
    except KeyError:
        pass

    return execution


@router.get("/invariants", response_model=List[SecurityInvariantDTO])
def list_security_invariants() -> List[SecurityInvariantDTO]:
    """Evaluates and lists platform security invariants."""
    return _invariants.evaluate_invariants()


@router.get("/drift", response_model=List[SecurityDriftDTO])
def list_security_drifts() -> List[SecurityDriftDTO]:
    """Lists detected security configuration and behavior drifts."""
    return _drift.list_drifts()


@router.get("/dependencies")
def get_control_dependencies() -> Dict[str, Any]:
    """Returns control dependency hierarchy and single points of failure."""
    return {
        "single_points_of_failure": _dependencies.identify_single_points_of_failure(),
    }


@router.get("/slo", response_model=List[SecuritySLODTO])
def list_security_slos() -> List[SecuritySLODTO]:
    """Returns security SLO metrics and error budgets."""
    return _slo.list_slos()
