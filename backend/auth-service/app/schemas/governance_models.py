"""Pydantic v2 DTO Schemas & Enums for Enterprise Governance (Phase 4.0 Part 8).

Defines canonical representations for Organization, RBAC, ABAC, Policy Engine,
Data Classification, Retention, Legal Hold, Audit, Compliance, Sessions, and API Keys.
"""

from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, ConfigDict
import uuid
from datetime import datetime, timezone

# ============================================================================
# Literal Types
# ============================================================================

OrganizationStatusLiteral = Literal[
    "ACTIVE",
    "SUSPENDED",
    "READ_ONLY",
    "DECOMMISSION_PENDING",
    "DECOMMISSIONED",
]

UserStatusLiteral = Literal[
    "INVITED",
    "ACTIVE",
    "SUSPENDED",
    "LOCKED",
    "DEACTIVATED",
    "DELETED",
    "PENDING_DELETION",
]

SystemRoleLiteral = Literal[
    "SUPER_ADMIN",
    "ORG_ADMIN",
    "SECURITY_ADMIN",
    "SOC_ANALYST",
    "SENIOR_ANALYST",
    "INVESTIGATOR",
    "THREAT_INTELLIGENCE_ANALYST",
    "INCIDENT_RESPONDER",
    "AUDITOR",
    "COMPLIANCE_OFFICER",
    "REPORT_VIEWER",
    "READ_ONLY_USER",
]

PermissionScopeLiteral = Literal[
    "ORGANIZATION",
    "TEAM",
    "CASE",
    "PROJECT",
    "RESOURCE",
    "ENTITY",
    "SELF",
    "GLOBAL",
]

DecisionEffectLiteral = Literal[
    "ALLOW",
    "DENY",
    "REQUIRE_APPROVAL",
    "REQUIRE_MFA",
    "READ_ONLY",
    "REQUIRE_STRONG_AUTH",
    "REQUIRE_TWO_PERSON_APPROVAL",
]

PolicyTypeLiteral = Literal[
    "ACCESS_CONTROL",
    "DATA_RETENTION",
    "EVIDENCE_RETENTION",
    "RESPONSE_AUTOMATION",
    "ALERT",
    "NOTIFICATION",
    "MFA",
    "SESSION",
    "API_ACCESS",
    "EXPORT",
    "DELETION",
    "COMPLIANCE",
    "PRIVACY",
    "INCIDENT",
    "PLAYBOOK",
]

DataClassificationLiteral = Literal[
    "PUBLIC",
    "INTERNAL",
    "CONFIDENTIAL",
    "RESTRICTED",
    "HIGHLY_RESTRICTED",
]

RetentionStateLiteral = Literal[
    "ACTIVE",
    "DUE_FOR_ARCHIVE",
    "ARCHIVED",
    "DUE_FOR_DELETION",
    "LEGAL_HOLD",
    "DELETION_PENDING",
    "DELETED",
    "RETENTION_EXCEPTION",
]

DeletionStatusLiteral = Literal[
    "DELETED",
    "PARTIALLY_DELETED",
    "PENDING",
    "FAILED",
    "BLOCKED",
    "UNKNOWN",
]

PrivacyRequestTypeLiteral = Literal[
    "ACCESS",
    "EXPORT",
    "RECTIFICATION",
    "DELETION",
    "RESTRICTION",
    "REVIEW",
]

ExportStatusLiteral = Literal[
    "PREPARING",
    "READY",
    "EXPIRED",
    "REVOKED",
    "FAILED",
]

GovernanceAlertTypeLiteral = Literal[
    "PRIVILEGE_ESCALATION",
    "MASS_EXPORT",
    "POLICY_CONFLICT",
    "UNAUTHORIZED_ACCESS",
    "AUDIT_TAMPERING_ATTEMPT",
    "EXCESSIVE_DENIALS",
    "UNUSUAL_ADMIN_ACTIVITY",
    "RETENTION_VIOLATION",
    "APPROVAL_ANOMALY",
    "API_KEY_ANOMALY",
]

ControlStatusLiteral = Literal[
    "NOT_ASSESSED",
    "NOT_APPLICABLE",
    "PARTIAL",
    "IMPLEMENTED",
    "VERIFIED",
    "FAILED",
    "EXCEPTION",
]

SessionStatusLiteral = Literal[
    "ACTIVE",
    "EXPIRED",
    "REVOKED",
    "SUSPENDED",
    "TERMINATED",
]

MFAPolicyLiteral = Literal[
    "MFA_OPTIONAL",
    "MFA_REQUIRED",
    "MFA_REQUIRED_FOR_ADMIN",
    "MFA_REQUIRED_FOR_SENSITIVE_ACTIONS",
    "MFA_REQUIRED_FOR_ALL_USERS",
]


# ============================================================================
# Organization & User DTOs (Sections 2, 3, 6, 7)
# ============================================================================

class OrganizationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: str = Field(default_factory=lambda: f"org_{uuid.uuid4().hex[:12]}")
    organization_name: str
    slug: str
    status: OrganizationStatusLiteral = "ACTIVE"
    plan: str = "ENTERPRISE"
    region: str = "ap-south-1"
    timezone: str = "Asia/Kolkata"
    data_residency: str = "IN"
    security_profile: Dict[str, Any] = Field(default_factory=dict)
    compliance_profile: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class UserLifecycleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: str = Field(default_factory=lambda: f"usr_{uuid.uuid4().hex[:12]}")
    organization_id: str
    email: str
    full_name: str = ""
    status: UserStatusLiteral = "ACTIVE"
    roles: List[str] = Field(default_factory=list)
    mfa_enforced: bool = False
    mfa_enabled: bool = False
    last_login_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# RBAC & ABAC DTOs (Sections 8-16)
# ============================================================================

class PermissionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    permission_id: str = Field(default_factory=lambda: f"perm_{uuid.uuid4().hex[:12]}")
    resource: str  # e.g., 'incident', 'report', 'evidence', 'policy', 'user'
    action: str    # e.g., 'read', 'write', 'delete', 'execute', 'approve'
    description: str = ""
    scope: PermissionScopeLiteral = "ORGANIZATION"


class RoleDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_id: str = Field(default_factory=lambda: f"role_{uuid.uuid4().hex[:12]}")
    organization_id: Optional[str] = None  # None for system default roles
    name: str
    description: str = ""
    system_role: bool = False
    permissions: List[str] = Field(default_factory=list)  # List of 'resource:action'
    scope: PermissionScopeLiteral = "ORGANIZATION"
    version: int = 1
    status: str = "ACTIVE"
    created_by: str = "SYSTEM"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class RoleVersionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version_id: str = Field(default_factory=lambda: f"rlv_{uuid.uuid4().hex[:12]}")
    role_id: str
    version_number: int
    content_hash: str
    permissions: List[str]
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuthorizationDecisionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    allowed: bool
    decision: DecisionEffectLiteral
    reason: str
    policy_id: Optional[str] = None
    policy_version: Optional[int] = None
    matched_rules: List[str] = Field(default_factory=list)
    required_permissions: List[str] = Field(default_factory=list)
    required_approval: bool = False
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Governance Policy & Simulation DTOs (Sections 17-26)
# ============================================================================

class GovernancePolicyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    policy_id: str = Field(default_factory=lambda: f"pol_{uuid.uuid4().hex[:12]}")
    organization_id: str
    name: str
    description: str = ""
    policy_type: PolicyTypeLiteral = "ACCESS_CONTROL"
    version: int = 1
    status: str = "ACTIVE"  # DRAFT, ACTIVE, DISABLED, ARCHIVED
    rules: List[Dict[str, Any]] = Field(default_factory=list)
    priority: int = 100  # Lower number = higher priority
    created_by: str = "ADMIN"
    approved_by: Optional[str] = None
    effective_from: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    effective_until: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyVersionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    version_id: str = Field(default_factory=lambda: f"plv_{uuid.uuid4().hex[:12]}")
    policy_id: str
    version_number: int
    content_hash: str
    rules: List[Dict[str, Any]]
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicySimulationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    simulation_id: str = Field(default_factory=lambda: f"psim_{uuid.uuid4().hex[:12]}")
    policy_id: str
    affected_users_count: int = 0
    affected_resources_count: int = 0
    new_denials_count: int = 0
    new_approvals_count: int = 0
    conflicts_detected: List[str] = Field(default_factory=list)
    simulation_verdict: str = "SIMULATION_PASSED_ZERO_MUTATION"
    simulated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyTestCaseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    test_id: str = Field(default_factory=lambda: f"ptst_{uuid.uuid4().hex[:12]}")
    policy_id: str
    input_context: Dict[str, Any]
    expected_decision: DecisionEffectLiteral
    actual_decision: Optional[DecisionEffectLiteral] = None
    status: str = "PENDING"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Data Classification & Retention DTOs (Sections 27-39)
# ============================================================================

class RetentionPolicyDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    policy_id: str = Field(default_factory=lambda: f"ret_{uuid.uuid4().hex[:12]}")
    organization_id: str
    resource_type: str  # 'ALERT', 'INCIDENT', 'REPORT', 'EVIDENCE', 'AUDIT_LOG'
    classification: DataClassificationLiteral = "INTERNAL"
    retention_period_days: int = 365
    deletion_strategy: str = "SOFT_DELETE"  # 'SOFT_DELETE', 'HARD_DELETE', 'ARCHIVE'
    legal_hold_behavior: str = "SHIELD_FROM_DELETION"
    archive_strategy: str = "COLD_STORAGE"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LegalHoldDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hold_id: str = Field(default_factory=lambda: f"hold_{uuid.uuid4().hex[:12]}")
    organization_id: str
    resource_type: str
    resource_id: str
    reason: str
    created_by: str
    approved_by: Optional[str] = None
    status: str = "ACTIVE"  # 'ACTIVE', 'RELEASED'
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    released_at: Optional[str] = None


class DataDeletionRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    deletion_id: str = Field(default_factory=lambda: f"del_{uuid.uuid4().hex[:12]}")
    organization_id: str
    resource_type: str
    resource_id: str
    requested_by: str
    approved_by: Optional[str] = None
    deletion_type: str = "PRIVACY_REQUEST"  # 'PRIVACY_REQUEST', 'RETENTION_EXPIRY', 'ADMIN_DELETION'
    status: DeletionStatusLiteral = "PENDING"
    verification_evidence: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class PrivacyRequestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    request_id: str = Field(default_factory=lambda: f"prv_{uuid.uuid4().hex[:12]}")
    organization_id: str
    data_principal_id: str
    request_type: PrivacyRequestTypeLiteral = "ACCESS"
    status: str = "PENDING"  # PENDING, IN_REVIEW, APPROVED, EXECUTING, COMPLETED, REJECTED
    identity_verified: bool = False
    legal_hold_checked: bool = False
    reason: str = ""
    assigned_to: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


class DataExportManifestDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    export_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:12]}")
    organization_id: str
    requester_id: str
    scope: str
    resource_count: int = 0
    classification: DataClassificationLiteral = "CONFIDENTIAL"
    integrity_hash: str
    status: ExportStatusLiteral = "READY"
    download_token: str = Field(default_factory=lambda: f"dlt_{uuid.uuid4().hex}")
    expires_at: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Audit Intelligence DTOs (Sections 45-52)
# ============================================================================

class AuditEventDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    audit_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:12]}")
    organization_id: str
    actor_type: str = "USER"  # USER, SERVICE_ACCOUNT, SYSTEM
    actor_id: str
    action: str  # e.g., 'login', 'response_execute', 'policy_publish', 'export'
    resource_type: str
    resource_id: str
    result: str = "SUCCESS"  # SUCCESS, DENIED, FAILED, BLOCKED
    reason: str = ""
    previous_hash: Optional[str] = None
    event_hash: str = ""
    session_reference: Optional[str] = None
    request_id: Optional[str] = None
    correlation_id: Optional[str] = None
    policy_id: Optional[str] = None
    policy_version: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AuditIntegrityCheckpointDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    checkpoint_id: str = Field(default_factory=lambda: f"chk_{uuid.uuid4().hex[:12]}")
    organization_id: str
    start_audit_id: str
    end_audit_id: str
    event_count: int
    merkle_root_hash: str
    verified: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class GovernanceAlertDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    alert_id: str = Field(default_factory=lambda: f"galt_{uuid.uuid4().hex[:12]}")
    organization_id: str
    alert_type: GovernanceAlertTypeLiteral
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    title: str
    description: str
    actor_id: Optional[str] = None
    affected_resource: Optional[str] = None
    status: str = "ACTIVE"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Compliance DTOs (Sections 53-62)
# ============================================================================

class ComplianceFrameworkDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    framework_id: str  # e.g., 'iso_27001', 'soc_2', 'nist_csf', 'cis_controls', 'dpdp_2023'
    name: str
    version: str = "2024"
    jurisdiction: str = "GLOBAL"
    description: str = ""
    control_count: int = 0
    status: str = "ACTIVE"


class ComplianceControlDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    control_id: str = Field(default_factory=lambda: f"ctrl_{uuid.uuid4().hex[:12]}")
    framework_id: str
    control_code: str  # e.g., 'A.9.1.1', 'CC6.1', 'PR.AC-1'
    title: str
    description: str = ""
    requirement: str = ""
    implementation_status: ControlStatusLiteral = "NOT_ASSESSED"
    evidence_requirements: List[str] = Field(default_factory=list)
    owner: str = "COMPLIANCE_LEAD"


class ComplianceEvidenceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    evidence_id: str = Field(default_factory=lambda: f"cev_{uuid.uuid4().hex[:12]}")
    control_id: str
    resource_type: str
    resource_id: str
    source: str
    integrity_hash: str
    valid_until: str
    status: str = "VERIFIED"
    collected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ComplianceAssessmentDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    assessment_id: str = Field(default_factory=lambda: f"cas_{uuid.uuid4().hex[:12]}")
    framework_id: str
    organization_id: str
    status: str = "COMPLETED"
    score_percentage: float = 0.0
    control_count: int = 0
    implemented_count: int = 0
    partial_count: int = 0
    failed_count: int = 0
    exception_count: int = 0
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    assessor: str = "AUTOMATED_GOVERNANCE_ENGINE"


class ComplianceReportDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_id: str = Field(default_factory=lambda: f"crep_{uuid.uuid4().hex[:12]}")
    framework_id: str
    organization_id: str
    executive_summary: str
    score_percentage: float
    control_breakdown: Dict[str, int]
    evidence_coverage_percentage: float
    gaps: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Session, Service Account & API Key DTOs (Sections 72-80)
# ============================================================================

class SessionGovernanceDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str = Field(default_factory=lambda: f"ses_{uuid.uuid4().hex[:12]}")
    user_id: str
    organization_id: str
    authentication_strength: str = "PASSWORD"  # PASSWORD, MFA_TOTP, SSO_OIDC
    mfa_verified: bool = False
    device_reference: str = "Unknown"
    ip_reference: str = "127.0.0.1"
    status: SessionStatusLiteral = "ACTIVE"
    expires_at: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ServiceAccountDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    service_account_id: str = Field(default_factory=lambda: f"sa_{uuid.uuid4().hex[:12]}")
    organization_id: str
    name: str
    description: str = ""
    permissions: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"
    created_by: str
    expires_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class APIKeyMetadataDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key_id: str = Field(default_factory=lambda: f"key_{uuid.uuid4().hex[:12]}")
    organization_id: str
    name: str
    key_prefix: str
    hashed_secret: str
    scope: str = "ORGANIZATION"
    permissions: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"  # ACTIVE, REVOKED, EXPIRED
    owner_id: str
    expires_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_used_at: Optional[str] = None


class APIKeyCreationResponseDTO(BaseModel):
    key_id: str
    name: str
    raw_key: str  # Returned ONLY ONCE upon creation! (Section 78, 91, Mandatory Test 12)
    key_prefix: str
    expires_at: Optional[str] = None


class GovernancePostureDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    organization_id: str
    overall_posture_score: float
    authorization_maturity: float
    policy_coverage: float
    mfa_coverage: float
    audit_coverage: float
    retention_coverage: float
    compliance_coverage: float
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
