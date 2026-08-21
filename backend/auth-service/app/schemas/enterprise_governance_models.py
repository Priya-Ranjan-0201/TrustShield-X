"""
TruthShield X — Enterprise Security & Compliance Operating System Schemas (Phase 32).

Strictly typed Pydantic models for Enterprise Controls, Continuous Control Monitoring,
Automated Evidence Management, Risk Register, Finding Remediation, Audit Requests,
Security Exceptions, and Regulatory Compliance Mapping.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 32)
# ============================================================================

ControlStatusLiteral = Literal[
    "DRAFT",
    "ACTIVE",
    "TESTING",
    "VERIFIED",
    "FAILED",
    "DEPRECATED",
    "RETIRED",
]

ControlEffectivenessLiteral = Literal[
    "EFFECTIVE",
    "PARTIALLY_EFFECTIVE",
    "INEFFECTIVE",
    "NOT_VERIFIED",
    "NOT_APPLICABLE",
]

FrameworkLiteral = Literal[
    "DPDP_2023",
    "ISO_27001",
    "SOC_2",
    "NIST_CSF",
    "NIST_AI_RMF",
    "CIS_CONTROLS",
]

MappingConfidenceLiteral = Literal[
    "DIRECT",
    "PARTIAL",
    "INDIRECT",
    "UNCERTAIN",
]

EvidenceFreshnessLiteral = Literal[
    "CURRENT",
    "EXPIRING",
    "EXPIRED",
    "UNKNOWN",
]

RiskStateLiteral = Literal[
    "IDENTIFIED",
    "ASSESSED",
    "TREATMENT_PLANNED",
    "MITIGATING",
    "ACCEPTED",
    "TRANSFERRED",
    "AVOIDED",
    "CLOSED",
    "REOPENED",
]


# ============================================================================
# Control Catalog & Testing
# ============================================================================

class ControlDTO(BaseModel):
    control_id: str = "ctrl_iam_mfa_enforcement"
    name: str = "Universal Multi-Factor Authentication Enforcement"
    description: str = "Mandates cryptographically backed MFA on all corporate and administrative sessions"
    primary_owner: str = "IAM_LEAD"
    backup_owner: str = "CISO_OPS"
    domain: str = "IDENTITY_AND_ACCESS"
    implementation_status: Literal["DESIGNED", "IMPLEMENTED", "CONFIGURED", "TESTED", "VERIFIED"] = "VERIFIED"
    effectiveness: ControlEffectivenessLiteral = "EFFECTIVE"
    risk_level: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    tenant_id: str = "default_tenant"
    status: ControlStatusLiteral = "ACTIVE"

    model_config = ConfigDict(frozen=True)


class ComplianceRequirementDTO(BaseModel):
    requirement_id: str = "req_iso27001_a9_4_2"
    framework: FrameworkLiteral = "ISO_27001"
    version: str = "2022"
    title: str = "User Authentication for External Connections"
    description: str = "Appropriate authentication methods shall be applied to control user access"
    mapped_controls: List[str] = Field(default_factory=lambda: ["ctrl_iam_mfa_enforcement"])
    evidence_requirements: List[str] = Field(default_factory=lambda: ["MFA configuration dump", "IdP audit logs"])
    confidence: MappingConfidenceLiteral = "DIRECT"
    status: Literal["COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT", "NOT_TESTED", "EVIDENCE_MISSING"] = "COMPLIANT"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Evidence Management & Audit Requests
# ============================================================================

class EvidenceDTO(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"evd_{uuid.uuid4().hex[:8]}")
    type: str = "CONFIGURATION_DUMP"
    source: str = "TruthShield Auth Service IAM Enclave"
    owner: str = "IAM_LEAD"
    classification: str = "RESTRICTED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validity_period_days: int = 90
    related_control: str = "ctrl_iam_mfa_enforcement"
    related_requirement: str = "req_iso27001_a9_4_2"
    integrity_hash: str = "c782b6b0c2e718b5b5c92ef9481283d5a498b375b485d99bfa210940562e84c9"
    freshness: EvidenceFreshnessLiteral = "CURRENT"
    status: Literal["VALID", "EXPIRED", "INTEGRITY_VIOLATION", "REDACTED"] = "VALID"

    model_config = ConfigDict(frozen=True)


class AuditRequestDTO(BaseModel):
    request_id: str = Field(default_factory=lambda: f"aud_req_{uuid.uuid4().hex[:8]}")
    auditor: str = "External Independent Audit Firm (SOC2 Type II)"
    requirement_id: str = "req_iso27001_a9_4_2"
    requested_evidence: str = "Provide active IdP configuration showing MFA enforcement policy"
    due_date: str = "2026-09-30T00:00:00Z"
    owner: str = "COMPLIANCE_OFFICER"
    status: Literal["REQUESTED", "ASSIGNED", "COLLECTING", "REVIEW", "SUBMITTED", "ACCEPTED", "CLOSED"] = "SUBMITTED"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Risk, Findings & Remediation
# ============================================================================

class EnterpriseRiskDTO(BaseModel):
    risk_id: str = "rsk_unauthorized_admin_access"
    title: str = "Risk of Administrative Account Compromise"
    description: str = "Risk that administrative access is gained via credential stuffing"
    asset: str = "Identity Provider & Tenant Management Gateway"
    threat: str = "Adversarial Credential Replay"
    vulnerability: str = "Legacy Single-Factor Legacy Protocols"
    control_id: str = "ctrl_iam_mfa_enforcement"
    likelihood: float = 0.20
    impact: float = 0.90
    inherent_risk: float = 0.85
    residual_risk: float = 0.18
    owner: str = "CISO"
    treatment: Literal["MITIGATE", "ACCEPT", "TRANSFER", "AVOID"] = "MITIGATE"
    status: RiskStateLiteral = "ASSESSED"

    model_config = ConfigDict(frozen=True)


class ComplianceFindingDTO(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"fnd_{uuid.uuid4().hex[:8]}")
    source: str = "Continuous Security Assurance Scanner"
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    confidence: float = 0.95
    affected_control: str = "ctrl_iam_mfa_enforcement"
    affected_asset: str = "Legacy Service Account svc_reports_01"
    risk_level: str = "HIGH"
    owner: str = "IAM_LEAD"
    status: Literal["OPEN", "IN_REMEDIATION", "VALIDATED", "CLOSED"] = "OPEN"

    model_config = ConfigDict(frozen=True)


class RemediationTaskDTO(BaseModel):
    task_id: str = Field(default_factory=lambda: f"rem_{uuid.uuid4().hex[:8]}")
    finding_id: str = "fnd_svc_account_legacy"
    action: str = "Migrate legacy service account to OAuth2 client credentials with certificate pinning"
    owner: str = "SECOPS_ENGINEER"
    priority: Literal["P0", "P1", "P2", "P3"] = "P1"
    sla_due_date: str = "2026-08-30T18:00:00Z"
    status: Literal["OPEN", "IN_PROGRESS", "READY_FOR_VALIDATION", "VERIFIED", "CLOSED"] = "IN_PROGRESS"
    is_verified: bool = False

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Exceptions, Third-Party Risk & Drift
# ============================================================================

class SecurityExceptionDTO(BaseModel):
    exception_id: str = Field(default_factory=lambda: f"exc_{uuid.uuid4().hex[:8]}")
    reason: str = "Temporary bypass for legacy mainframe telemetry probe during migration"
    scope: str = "Host probe 10.0.12.44"
    owner: str = "INFRA_LEAD"
    compensating_controls: List[str] = Field(default_factory=lambda: ["Network micro-segmentation", "Deep packet inspection probe"])
    approved_by: str = "CISO"
    expiration_date: str = "2026-09-01T00:00:00Z"
    status: Literal["ACTIVE", "EXPIRING", "EXPIRED", "REVOKED"] = "ACTIVE"

    model_config = ConfigDict(frozen=True)


class ThirdPartyRiskDTO(BaseModel):
    vendor_id: str = "vnd_cloud_storage_aws"
    vendor_name: str = "Amazon Web Services Inc."
    service: str = "S3 Encrypted Object Store"
    data_access_level: str = "CONFIDENTIAL_ENCRYPTED"
    criticality: Literal["TIER_1", "TIER_2", "TIER_3"] = "TIER_1"
    risk_level: str = "LOW"
    assessment_status: Literal["APPROVED", "UNDER_REVIEW", "CONDITIONAL", "REJECTED"] = "APPROVED"

    model_config = ConfigDict(frozen=True)


class ComplianceSnapshotDTO(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: f"snp_{uuid.uuid4().hex[:8]}")
    framework: FrameworkLiteral = "SOC_2"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    compliant_count: int = 42
    non_compliant_count: int = 0
    evidence_missing_count: int = 0

    model_config = ConfigDict(frozen=True)


class ComplianceDriftEventDTO(BaseModel):
    drift_id: str = Field(default_factory=lambda: f"drf_{uuid.uuid4().hex[:8]}")
    control_id: str = "ctrl_iam_mfa_enforcement"
    previous_state: str = "VERIFIED"
    current_state: str = "DEGRADED"
    severity: str = "HIGH"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
