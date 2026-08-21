"""
TruthShield X — Phase 34: Zero-Trust & Continuous Exposure Management Models
=============================================================================
Unified Pydantic models for Continuous Identity Security, Device Trust,
Session Security, Service Identity, Privilege Governance, Microsegmentation,
Zero-Trust Decisions, EASM, Asset Discovery, Exposure Management,
Vulnerability Exposure Correlation, Attack-Path Analysis, Blast Radius,
Continuous Exposure Monitoring, and Remediation Validation.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class IdentityProfileDTO(BaseModel):
    identity_id: str
    tenant_id: str
    username: str
    email: str
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    risk_score: float = 0.0
    identity_trust_state: str = "TRUSTED"  # TRUSTED, CONDITIONAL, IDENTITY_UNTRUSTED, COMPROMISED
    mfa_enforced: bool = True
    last_authenticated_at: Optional[str] = None
    known_devices: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class DeviceTrustDTO(BaseModel):
    device_id: str
    tenant_id: str
    owner_id: str
    hostname: str
    os_name: str
    os_version: str
    trust_state: str = "UNKNOWN"  # TRUSTED, CONDITIONAL, UNTRUSTED, COMPROMISED, QUARANTINED, UNKNOWN
    encryption_enabled: bool = False
    patch_compliant: bool = False
    edr_active: bool = False
    certificate_valid: bool = False
    posture_score: float = 0.0
    last_posture_assessment: Optional[str] = None
    quarantine_reason: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SessionSecurityDTO(BaseModel):
    session_id: str
    tenant_id: str
    user_id: str
    device_id: str
    ip_address: str
    auth_strength: str = "PWD_MFA"  # PWD, PWD_MFA, PASSKEY_FIDO2, CERTIFICATE
    state: str = "ACTIVE"  # ACTIVE, ELEVATED, SUSPENDED, REAUTH_REQUIRED, TERMINATED, QUARANTINED
    risk_score: float = 0.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_activity_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    impossible_travel_detected: bool = False
    privilege_level: str = "STANDARD"


class ServiceIdentityDTO(BaseModel):
    service_id: str
    tenant_id: str
    service_name: str
    spiffe_id: str
    environment: str = "PRODUCTION"  # DEV, STAGING, PRODUCTION
    allowed_callers: List[str] = Field(default_factory=list)
    allowed_targets: List[str] = Field(default_factory=list)
    certificate_fingerprint: str
    mtls_enforced: bool = True
    least_privilege_compliant: bool = True
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class JITPrivilegeDTO(BaseModel):
    request_id: str
    tenant_id: str
    user_id: str
    target_role: str
    justification: str
    duration_minutes: int
    approval_status: str = "PENDING"  # PENDING, APPROVED, REJECTED, EXPIRED, REVOKED
    approved_by: Optional[str] = None
    expires_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class NetworkSegmentDTO(BaseModel):
    segment_id: str
    tenant_id: str
    name: str
    trust_zone: str  # INTERNET, DMZ, USER, APPLICATION, DATABASE, ADMIN, MANAGEMENT, SECURITY, RESTRICTED
    allowed_ingress_zones: List[str] = Field(default_factory=list)
    allowed_egress_zones: List[str] = Field(default_factory=list)
    enforce_mtls: bool = True
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ZeroTrustDecisionDTO(BaseModel):
    decision_id: str
    tenant_id: str
    correlation_id: str
    subject_id: str
    device_id: str
    session_id: str
    resource_id: str
    action: str
    decision: str  # ALLOW, DENY, STEP_UP, REAUTHENTICATE, QUARANTINE, HUMAN_REVIEW
    decision_reason: str
    policy_name: str
    confidence: float
    required_action: Optional[str] = None
    trust_scores: Dict[str, float] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ExternalAssetDTO(BaseModel):
    asset_id: str
    tenant_id: str
    asset_type: str  # DOMAIN, SUBDOMAIN, PUBLIC_IP, CERTIFICATE, CLOUD_STORAGE, API_ENDPOINT, PUBLIC_SERVICE
    identifier: str
    discovery_method: str = "PASSIVE_DISCOVERY"  # PASSIVE_DISCOVERY, ACTIVE_DISCOVERY
    confidence: float = 1.0
    owner: str = "UNKNOWN"
    environment: str = "EXTERNAL"
    criticality: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    is_known_in_inventory: bool = True
    technologies: List[Dict[str, Any]] = Field(default_factory=list)
    first_seen: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ExposureFindingDTO(BaseModel):
    exposure_id: str
    tenant_id: str
    asset_id: str
    exposure_type: str  # PUBLICLY_REACHABLE, MISCONFIGURED, EXPOSED_ADMIN_INTERFACE, EXPOSED_SERVICE, EXPOSED_SECRET, EXPOSED_STORAGE, EXPOSED_API, EXPIRED_CERTIFICATE, UNKNOWN_ASSET
    severity: str = "HIGH"  # LOW, MEDIUM, HIGH, CRITICAL
    reachability: str = "NOT_VERIFIED"  # REACHABLE, BLOCKED, NOT_VERIFIED
    business_impact: str = "MEDIUM"
    status: str = "OPEN"  # OPEN, MITIGATED, RESOLVED, SUPPRESSED
    details: Dict[str, Any] = Field(default_factory=dict)
    discovered_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class VulnerabilityExposureDTO(BaseModel):
    correlation_id: str
    tenant_id: str
    asset_id: str
    cve_id: str
    cvss_score: float
    epss_probability: float
    exposure_type: str
    exploitability: str = "EXPLOITABILITY_UNVERIFIED"  # UNKNOWN, POSSIBLE, LIKELY, VERIFIED, EXPLOITABILITY_UNVERIFIED
    exploit_evidence: Optional[Dict[str, Any]] = None
    composite_risk_score: float = 0.0
    correlated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class AttackPathDTO(BaseModel):
    path_id: str
    tenant_id: str
    entry_point: str
    target_crown_jewel: str
    path_type: str = "NETWORK"  # NETWORK, IDENTITY, APPLICATION, CLOUD, DATA, SERVICE, HYBRID
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "ATTACK_PATH_UNVERIFIED"  # SIMULATED, PROBABLE, VERIFIED, ATTACK_PATH_UNVERIFIED
    reachability_verified: bool = False
    evidence: List[Dict[str, Any]] = Field(default_factory=list)
    risk_score: float = 0.0
    discovered_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class CrownJewelDTO(BaseModel):
    jewel_id: str
    tenant_id: str
    name: str
    resource_type: str  # DATABASE, REPOSITORY, IDENTITY_PROVIDER, CIPHER_KEYSTORE, RESTRICTED_SERVICE
    sensitivity: str = "RESTRICTED"  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED
    business_criticality: str = "CRITICAL"
    owner: str
    blast_radius_factor: float = 1.0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class BlastRadiusDTO(BaseModel):
    calculation_id: str
    tenant_id: str
    source_asset_id: str
    mode: str = "SIMULATED"  # OBSERVED, POSSIBLE, SIMULATED
    reachable_assets: List[str] = Field(default_factory=list)
    reachable_identities: List[str] = Field(default_factory=list)
    reachable_crown_jewels: List[str] = Field(default_factory=list)
    risk_multiplication_factor: float = 1.0
    calculated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ExposureDriftDTO(BaseModel):
    drift_id: str
    tenant_id: str
    asset_id: str
    drift_type: str  # EXPOSURE_DRIFT, ZERO_TRUST_DRIFT, PRIVILEGE_DRIFT, CERTIFICATE_EXPIRATION
    previous_state: Dict[str, Any]
    current_state: Dict[str, Any]
    detected_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class RemediationActionDTO(BaseModel):
    action_id: str
    tenant_id: str
    exposure_id: str
    recommendation_type: str  # PATCH, CONFIGURE, RESTRICT_ACCESS, REMOVE_EXPOSURE, ROTATE_CREDENTIAL, SEGMENT, DISABLE_SERVICE, MONITOR, INVESTIGATE
    title: str
    description: str
    status: str = "PENDING"  # PENDING, IN_PROGRESS, VALIDATION_REQUIRED, VERIFIED, BLOCKED
    validation_status: str = "REMEDIATION_NOT_VERIFIED"  # REMEDIATION_NOT_VERIFIED, RESCAN_PENDING, CONFIRMED_REMEDIATED
    evidence: Optional[Dict[str, Any]] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ContinuousTrustScorecardDTO(BaseModel):
    scorecard_id: str
    tenant_id: str
    subject_id: str
    identity_trust: float
    device_trust: float
    session_trust: float
    resource_risk: float
    exposure_level: float
    policy_compliance: float
    threat_context_score: float
    overall_confidence: float
    evaluated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
