"""
TruthShield X — Release Guardian REST API Endpoints
====================================================
Exposes endpoints for:
- Release candidate ingestion and management
- Impact analysis and targeted test discovery
- Multi-dimensional gate evaluation (Security, AI, Performance, Findings)
- Four-eyes human governance approval
- Controlled deployment and verified rollback
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from app.services.release_guardian import (
    release_guardian_engine,
    ReleaseCandidateStatus,
)

router = APIRouter(prefix="/releases", tags=["Release Guardian & Governance"])


class CreateReleaseRequest(BaseModel):
    version: str
    commit_hash: str
    author: str
    changed_components: List[str]
    change_types: List[str]
    description: Optional[str] = ""
    raw_manifest: Optional[Dict[str, Any]] = None


class EvaluateReleaseRequest(BaseModel):
    test_execution_results: Optional[Dict[str, Any]] = None
    adversarial_probe_results: Optional[Dict[str, Any]] = None


class ApproveReleaseRequest(BaseModel):
    approver: str
    role: str
    justification: str


class BlockReleaseRequest(BaseModel):
    reason: str
    blocked_by: str


class DeployReleaseRequest(BaseModel):
    deployed_by: str


class RollbackReleaseRequest(BaseModel):
    reason: str
    authorized_by: str


@router.get("")
async def list_releases() -> Dict[str, Any]:
    """Lists all registered Release Candidates and their gate statuses."""
    candidates = release_guardian_engine.get_candidates()
    return {"releases_count": len(candidates), "releases": candidates}


@router.post("")
async def create_release_candidate(request: CreateReleaseRequest) -> Dict[str, Any]:
    """Ingests a new Release Candidate across 17 vectors and computes risk & impact."""
    return release_guardian_engine.create_release_candidate(
        version=request.version,
        commit_hash=request.commit_hash,
        author=request.author,
        changed_components=request.changed_components,
        change_types=request.change_types,
        description=request.description or "",
        raw_manifest=request.raw_manifest
    )


@router.get("/{id}")
async def get_release(id: str) -> Dict[str, Any]:
    """Retrieves full candidate details, gate results, and approval records."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    return candidate


@router.get("/{id}/impact")
async def get_release_impact(id: str) -> Dict[str, Any]:
    """Retrieves the CHANGE_IMPACT_GRAPH and affected controls for the release."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    return {"release_id": id, "impact_graph": candidate.get("impact_graph", {})}


@router.get("/{id}/tests")
async def get_release_tests(id: str) -> Dict[str, Any]:
    """Retrieves selected regression test suites for the release."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    return {"release_id": id, "tests_selected": candidate.get("tests_selected", [])}


@router.get("/{id}/security")
async def get_release_security(id: str) -> Dict[str, Any]:
    """Retrieves security invariant gate results and tenant isolation status."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    gates = candidate.get("gate_results", {})
    return {
        "release_id": id,
        "security_gate": gates.get("CRITICAL_SECURITY_GATE", "NOT_VERIFIED"),
        "tenant_isolation_gate": gates.get("TENANT_ISOLATION_GATE", "NOT_VERIFIED"),
        "authorization_gate": gates.get("AUTHORIZATION_GATE", "NOT_VERIFIED"),
    }


@router.get("/{id}/ai")
async def get_release_ai(id: str) -> Dict[str, Any]:
    """Retrieves AI safety evaluation and golden dataset benchmark results."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    gates = candidate.get("gate_results", {})
    return {
        "release_id": id,
        "ai_safety_gate": gates.get("AI_SAFETY_GATE", "NOT_VERIFIED"),
    }


@router.get("/{id}/performance")
async def get_release_performance(id: str) -> Dict[str, Any]:
    """Retrieves performance regression analysis and latency profile."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    gates = candidate.get("gate_results", {})
    return {
        "release_id": id,
        "performance_gate": gates.get("PERFORMANCE_GATE", "NOT_VERIFIED"),
    }


@router.get("/{id}/findings")
async def get_release_findings(id: str) -> Dict[str, Any]:
    """Retrieves release blockers, deviations, and unresolved findings."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    return {
        "release_id": id,
        "blockers": candidate.get("blockers", []),
        "findings": candidate.get("findings", []),
    }


@router.post("/{id}/evaluate")
async def evaluate_release(id: str, request: EvaluateReleaseRequest) -> Dict[str, Any]:
    """Executes all 13 Release Guardian gates against the release candidate."""
    result = release_guardian_engine.evaluate_release_candidate(
        release_id=id,
        test_execution_results=request.test_execution_results or {"test_integrity_valid": True},
        adversarial_probe_results=request.adversarial_probe_results
    )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/{id}/approve")
async def approve_release(id: str, request: ApproveReleaseRequest) -> Dict[str, Any]:
    """Records human four-eyes approval (AI agents strictly prohibited)."""
    result = release_guardian_engine.record_human_approval(
        release_id=id,
        approver=request.approver,
        role=request.role,
        justification=request.justification
    )
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Approval failed"))
    return result


@router.post("/{id}/block")
async def block_release(id: str, request: BlockReleaseRequest) -> Dict[str, Any]:
    """Explicitly blocks a release candidate with justification."""
    candidate = release_guardian_engine.get_candidate(id)
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Release {id} not found")
    candidate["status"] = ReleaseCandidateStatus.BLOCKED.value
    candidate["blockers"].append({"gate": "MANUAL_BLOCK", "reason": request.reason, "blocked_by": request.blocked_by})
    return {"release_id": id, "status": "BLOCKED", "reason": request.reason}


@router.post("/{id}/deploy")
async def deploy_release(id: str, request: DeployReleaseRequest) -> Dict[str, Any]:
    """Deploys an approved release candidate with post-deployment sanity validation."""
    result = release_guardian_engine.deploy_release(release_id=id, deployed_by=request.deployed_by)
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Deployment failed"))
    return result


@router.post("/{id}/rollback")
async def rollback_release(id: str, request: RollbackReleaseRequest) -> Dict[str, Any]:
    """Rolls back a release candidate to the last certified safe baseline."""
    return release_guardian_engine.rollback_release(
        release_id=id,
        reason=request.reason,
        authorized_by=request.authorized_by
    )
