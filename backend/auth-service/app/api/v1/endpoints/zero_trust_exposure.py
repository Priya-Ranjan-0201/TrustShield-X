"""
Zero-Trust & Continuous Exposure Endpoints (Phase 34)
=====================================================
Exposes comprehensive REST APIs for Zero-Trust Decisions, Continuous Identity,
Device Trust, Sessions, JIT Privileges, Microsegmentation, EASM, Asset Discovery,
Exposure Management, Vulnerability Correlation, Attack Paths, Security Graph, and Verified Remediation.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from pydantic import BaseModel

from app.services.zero_trust_exposure.zero_trust_security_engine import zero_trust_security_engine
from app.schemas.zero_trust_exposure_models import (
    IdentityProfileDTO, DeviceTrustDTO, SessionSecurityDTO,
    ZeroTrustDecisionDTO, ServiceIdentityDTO, JITPrivilegeDTO,
    ExternalAssetDTO, ExposureFindingDTO, VulnerabilityExposureDTO,
    AttackPathDTO, BlastRadiusDTO, RemediationActionDTO,
    ContinuousTrustScorecardDTO
)

router = APIRouter(prefix="/zero-trust-exposure", tags=["Zero-Trust & Continuous Exposure Control Plane"])


class AccessEvaluationRequest(BaseModel):
    tenant_id: str
    subject_id: str
    device_id: str
    session_id: str
    resource_id: str
    resource_sensitivity: str
    action: str
    source_ip: str
    auth_context: Optional[Dict[str, Any]] = None
    device_telemetry: Optional[Dict[str, Any]] = None


# 1. Access Decisions & Scorecard
@router.post("/evaluate-access", response_model=Dict[str, Any])
async def evaluate_access(req: AccessEvaluationRequest):
    return zero_trust_security_engine.evaluate_unified_access_request(
        tenant_id=req.tenant_id,
        subject_id=req.subject_id,
        device_id=req.device_id,
        session_id=req.session_id,
        resource_id=req.resource_id,
        resource_sensitivity=req.resource_sensitivity,
        action=req.action,
        source_ip=req.source_ip,
        auth_context=req.auth_context,
        device_telemetry=req.device_telemetry
    )


@router.get("/decisions/{tenant_id}", response_model=List[Dict[str, Any]])
async def list_decisions(tenant_id: str):
    return zero_trust_security_engine.decision_engine.get_decisions(tenant_id)


@router.get("/scorecard/{tenant_id}/{subject_id}", response_model=Dict[str, Any])
async def get_trust_scorecard(tenant_id: str, subject_id: str):
    return zero_trust_security_engine.generate_trust_scorecard(tenant_id, subject_id)


# 2. Identity Security
@router.post("/identities/register", response_model=Dict[str, Any])
async def register_identity(data: Dict[str, Any]):
    return zero_trust_security_engine.identity_engine.register_identity(
        identity_id=data.get("identity_id", "ID-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        username=data.get("username", "user"),
        email=data.get("email", "user@truthshield.io"),
        roles=data.get("roles", ["USER"]),
        permissions=data.get("permissions", ["read:data"]),
        mfa_enforced=data.get("mfa_enforced", True)
    )


@router.get("/identities/{tenant_id}/{subject_id}", response_model=Dict[str, Any])
async def get_identity(tenant_id: str, subject_id: str):
    ident = zero_trust_security_engine.identity_engine.get_identity(subject_id, tenant_id)
    if not ident:
        raise HTTPException(status_code=404, detail="Identity not found")
    return ident


# 3. Device Trust
@router.post("/devices/register", response_model=Dict[str, Any])
async def register_device(data: Dict[str, Any]):
    return zero_trust_security_engine.device_engine.register_device(
        device_id=data.get("device_id", "DEV-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        owner_id=data.get("owner_id", "user-default"),
        hostname=data.get("hostname", "host.domain.internal"),
        os_name=data.get("os_name", "Linux"),
        os_version=data.get("os_version", "Ubuntu 22.04"),
        edr_active=data.get("edr_active", True),
        disk_encrypted=data.get("disk_encrypted", True),
        firewall_active=data.get("firewall_active", True),
        patch_compliant=data.get("patch_compliant", True),
        certificate_valid=data.get("certificate_valid", True)
    )


@router.post("/devices/posture", response_model=Dict[str, Any])
async def assess_device_posture(data: Dict[str, Any]):
    return zero_trust_security_engine.device_engine.assess_posture(
        device_id=data.get("device_id", "DEV-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        telemetry=data.get("telemetry", {})
    )


@router.post("/devices/quarantine", response_model=Dict[str, Any])
async def quarantine_device(data: Dict[str, Any]):
    return zero_trust_security_engine.device_engine.quarantine_device(
        device_id=data.get("device_id", "DEV-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        reason=data.get("reason", "COMPROMISE_DETECTED")
    )


# 4. Sessions
@router.post("/sessions/create", response_model=Dict[str, Any])
async def create_session(data: Dict[str, Any]):
    return zero_trust_security_engine.session_engine.create_session(
        session_id=data.get("session_id", "SESS-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        subject_id=data.get("subject_id", "user-default"),
        device_id=data.get("device_id", "DEV-DEFAULT"),
        source_ip=data.get("source_ip", "127.0.0.1"),
        initial_risk_score=data.get("initial_risk_score", 0.0)
    )


@router.post("/sessions/evaluate", response_model=Dict[str, Any])
async def evaluate_session(data: Dict[str, Any]):
    return zero_trust_security_engine.session_engine.evaluate_session_activity(
        session_id=data.get("session_id", "SESS-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        current_ip=data.get("current_ip", "127.0.0.1"),
        current_device=data.get("current_device", "DEV-DEFAULT"),
        activity_type=data.get("activity_type", "READ"),
        risk_signals=data.get("risk_signals", [])
    )


@router.post("/sessions/revoke", response_model=Dict[str, Any])
async def revoke_session(data: Dict[str, Any]):
    return zero_trust_security_engine.session_engine.revoke_session(
        session_id=data.get("session_id", "SESS-DEFAULT"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        reason=data.get("reason", "MANUAL_REVOCATION")
    )


# 5. EASM & External Assets
@router.post("/easm/discover", response_model=Dict[str, Any])
async def discover_external_asset(data: Dict[str, Any]):
    return zero_trust_security_engine.easm_engine.discover_asset(
        asset_id=data.get("asset_id", "EXT-ASSET-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        identifier=data.get("identifier", "api.truthshield.io"),
        asset_type=data.get("asset_type", "DOMAIN"),
        discovery_method=data.get("discovery_method", "PASSIVE_DISCOVERY"),
        confidence=data.get("confidence", 1.0),
        owner=data.get("owner", "SecOps"),
        criticality=data.get("criticality", "HIGH"),
        open_ports=data.get("open_ports"),
        technologies=data.get("technologies")
    )


@router.get("/easm/assets/{tenant_id}", response_model=List[Dict[str, Any]])
async def list_external_assets(tenant_id: str):
    return zero_trust_security_engine.easm_engine.get_external_assets(tenant_id)


@router.get("/easm/shadow-it/{tenant_id}", response_model=List[Dict[str, Any]])
async def detect_shadow_it(tenant_id: str):
    return zero_trust_security_engine.easm_engine.detect_shadow_it(tenant_id)


@router.get("/assets/unknown/{tenant_id}", response_model=List[Dict[str, Any]])
async def get_unknown_assets(tenant_id: str):
    return zero_trust_security_engine.asset_inventory_engine.get_unknown_assets(tenant_id)


# 6. Exposure Management
@router.post("/exposures/record", response_model=Dict[str, Any])
async def record_exposure(data: Dict[str, Any]):
    return zero_trust_security_engine.exposure_engine.record_exposure(
        exposure_id=data.get("exposure_id", "EXP-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        asset_id=data.get("asset_id", "EXT-ASSET-01"),
        exposure_type=data.get("exposure_type", "PUBLICLY_REACHABLE"),
        severity=data.get("severity", "HIGH"),
        reachability_evidence=data.get("reachability_evidence"),
        business_impact=data.get("business_impact", "HIGH")
    )


@router.get("/exposures/open/{tenant_id}", response_model=List[Dict[str, Any]])
async def list_open_exposures(tenant_id: str):
    return zero_trust_security_engine.exposure_engine.get_open_exposures(tenant_id)


# 7. Vulnerability Exposure Correlation
@router.post("/vulnerabilities/correlate", response_model=Dict[str, Any])
async def correlate_vulnerability(data: Dict[str, Any]):
    return zero_trust_security_engine.vuln_correlation_engine.correlate_vulnerability(
        correlation_id=data.get("correlation_id", "VCORR-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        asset_id=data.get("asset_id", "EXT-ASSET-01"),
        cve_id=data.get("cve_id", "CVE-2024-3094"),
        cvss_score=data.get("cvss_score", 10.0),
        epss_probability=data.get("epss_probability", 0.95),
        exposure_type=data.get("exposure_type", "PUBLICLY_REACHABLE"),
        exploit_evidence=data.get("exploit_evidence")
    )


# 8. Attack Paths & Blast Radius
@router.post("/attack-paths/analyze", response_model=Dict[str, Any])
async def analyze_attack_path(data: Dict[str, Any]):
    return zero_trust_security_engine.attack_path_engine.analyze_path(
        path_id=data.get("path_id", "PATH-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        entry_point=data.get("entry_point", "EXT-ASSET-01"),
        target_crown_jewel=data.get("target_crown_jewel", "DB-MAIN"),
        path_type=data.get("path_type", "NETWORK"),
        nodes=data.get("nodes", []),
        edges=data.get("edges", []),
        evidence=data.get("evidence", []),
        is_ai_generated=data.get("is_ai_generated", False),
        is_simulation=data.get("is_simulation", False)
    )


@router.get("/attack-paths/{tenant_id}", response_model=List[Dict[str, Any]])
async def list_attack_paths(tenant_id: str):
    return zero_trust_security_engine.attack_path_engine.get_paths(tenant_id)


@router.get("/attack-paths/{tenant_id}/{path_id}", response_model=Dict[str, Any])
async def get_attack_path(tenant_id: str, path_id: str):
    path = zero_trust_security_engine.attack_path_engine.get_path(path_id, tenant_id)
    if not path:
        raise HTTPException(status_code=404, detail="Attack path not found")
    return path


@router.post("/blast-radius/calculate", response_model=Dict[str, Any])
async def calculate_blast_radius(data: Dict[str, Any]):
    return zero_trust_security_engine.blast_radius_engine.calculate_blast_radius(
        node_id=data.get("node_id", "NODE-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        neighbors=data.get("neighbors", []),
        data_stores=data.get("data_stores", []),
        credentials_scope=data.get("credentials_scope", "LOCAL")
    )


# 9. JIT Privilege & Break-Glass Access
@router.post("/privilege/jit/request", response_model=Dict[str, Any])
async def request_jit_privilege(data: Dict[str, Any]):
    return zero_trust_security_engine.privilege_engine.request_jit_privilege(
        request_id=data.get("request_id", "JIT-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        subject_id=data.get("subject_id", "user-default"),
        target_role=data.get("target_role", "SECURITY_ADMIN"),
        duration_minutes=data.get("duration_minutes", 30),
        justification=data.get("justification", "Emergency access")
    )


@router.post("/privilege/break-glass", response_model=Dict[str, Any])
async def request_break_glass(data: Dict[str, Any]):
    return zero_trust_security_engine.privilege_engine.request_break_glass_access(
        event_id=data.get("event_id", "BG-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        subject_id=data.get("subject_id", "user-default"),
        justification=data.get("justification", "P1 outage incident response"),
        mfa_token=data.get("mfa_token", "998822"),
        duration_minutes=data.get("duration_minutes", 15)
    )


# 10. Drift Monitoring
@router.post("/exposure/drift", response_model=Dict[str, Any])
async def check_drift(data: Dict[str, Any]):
    return zero_trust_security_engine.drift_engine.check_exposure_drift(
        drift_id=data.get("drift_id", "DRIFT-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        asset_id=data.get("asset_id", "EXT-ASSET-01"),
        previous_state=data.get("previous_state", {}),
        current_state=data.get("current_state", {})
    )


# 11. Remediation Validation
@router.post("/remediations/verify", response_model=Dict[str, Any])
async def verify_remediation(data: Dict[str, Any]):
    return zero_trust_security_engine.remediation_engine.verify_remediation(
        action_id=data.get("action_id", "ACT-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        rescan_telemetry=data.get("rescan_telemetry")
    )


# 12. Security Graph
@router.post("/graph/nodes/add", response_model=Dict[str, Any])
async def add_graph_node(data: Dict[str, Any]):
    return zero_trust_security_engine.security_graph.add_node(
        tenant_id=data.get("tenant_id", "tenant-default"),
        node_id=data.get("node_id", "NODE-01"),
        node_type=data.get("node_type", "ASSET"),
        properties=data.get("properties")
    )


@router.post("/graph/edges/add", response_model=Dict[str, Any])
async def add_graph_edge(data: Dict[str, Any]):
    return zero_trust_security_engine.security_graph.add_edge(
        tenant_id=data.get("tenant_id", "tenant-default"),
        edge_id=data.get("edge_id", "EDGE-01"),
        source_node_id=data.get("source_node_id", "NODE-01"),
        target_node_id=data.get("target_node_id", "NODE-02"),
        edge_type=data.get("edge_type", "CONNECTS_TO"),
        confidence=data.get("confidence", 1.0),
        evidence=data.get("evidence")
    )


@router.get("/graph/{tenant_id}", response_model=Dict[str, Any])
async def get_graph(tenant_id: str):
    nodes = zero_trust_security_engine.security_graph.get_nodes(tenant_id)
    edges = zero_trust_security_engine.security_graph.get_edges(tenant_id)
    return {"tenant_id": tenant_id, "nodes": nodes, "edges": edges}
