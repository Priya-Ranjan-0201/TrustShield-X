"""
TruthShield X — Phase 14 Continuous Security Governance & Compliance Evidence Automation Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


RequirementStatusLiteral = Literal[
    "NOT_ASSESSED",
    "PARTIALLY_SATISFIED",
    "SATISFIED",
    "NOT_SATISFIED",
    "NOT_APPLICABLE",
    "UNKNOWN",
]

EvidenceFreshnessLiteral = Literal[
    "CURRENT",
    "STALE",
    "EXPIRED",
    "INVALID",
    "UNKNOWN",
]

ExceptionStatusLiteral = Literal[
    "REQUESTED",
    "UNDER_REVIEW",
    "APPROVED",
    "REJECTED",
    "ACTIVE",
    "EXPIRED",
    "REVOKED",
    "CLOSED",
]

RemediationStatusLiteral = Literal[
    "OPEN",
    "ASSIGNED",
    "IN_PROGRESS",
    "BLOCKED",
    "READY_FOR_VERIFICATION",
    "VERIFIED",
    "REJECTED",
    "CLOSED",
]


class GovernanceFrameworkDTO(BaseModel):
    framework_id: str
    name: str  # DPDP 2023, ISO 27001:2022, SOC 2 Type II, NIST CSF 2.0, CIS Controls v8
    version: str = "2023"
    effective_date: str = "2023-08-11"
    source_reference: str
    status: Literal["ACTIVE", "DRAFT", "DEPRECATED"] = "ACTIVE"
    total_requirements: int = 5


class GovernanceRequirementDTO(BaseModel):
    requirement_id: str
    framework_id: str
    framework_version: str = "2023"
    control_reference: str
    title: str
    description: str
    category: str
    applicability: Literal["ALL_TENANTS", "ENTERPRISE_ONLY", "HEALTHCARE_ONLY", "FINANCIAL_ONLY"] = "ALL_TENANTS"
    owner: str = "compliance_lead"
    status: RequirementStatusLiteral = "SATISFIED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ControlMappingDTO(BaseModel):
    mapping_id: str
    requirement_id: str
    control_id: str
    assertion_id: str
    test_id: str
    evidence_id: str
    confidence_weight: float = 1.0


class GovernanceEvidenceDTO(BaseModel):
    evidence_id: str
    control_id: str
    tenant_id: str = "PLATFORM_SCOPE"
    source_system: str
    collected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    valid_until: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    freshness: EvidenceFreshnessLiteral = "CURRENT"
    integrity_hash: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class EvidenceChainDTO(BaseModel):
    chain_id: str
    requirement_id: str
    control_id: str
    assertion: str
    test_execution_id: str
    evidence_id: str
    is_valid: bool = True
    chain_hash: str


class GovernanceExceptionDTO(BaseModel):
    exception_id: str
    requirement_id: str
    control_id: str
    reason: str
    business_justification: str
    risk_acceptance: str
    owner: str
    approver: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiration: str
    status: ExceptionStatusLiteral = "ACTIVE"
    compensating_control_id: Optional[str] = None


class GovernanceRemediationDTO(BaseModel):
    remediation_id: str
    finding_title: str
    requirement_id: str
    owner: str
    priority: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    due_date: str
    action_plan: str
    status: RemediationStatusLiteral = "OPEN"
    verification_evidence_id: Optional[str] = None


class AuditPackageDTO(BaseModel):
    package_id: str
    framework_id: str
    framework_version: str
    scope: str = "FULL_ENTERPRISE_TENANT_ISOLATION"
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_requirements_assessed: int
    requirements_satisfied: int
    requirements_partial: int
    requirements_not_satisfied: int
    active_exceptions_count: int
    integrity_manifest_hash: str
    limitations: List[str] = Field(default_factory=list)


class GovernancePostureSummaryDTO(BaseModel):
    governance_posture_score: float  # 0.0 - 100.0
    compliance_confidence: float  # 0.0 - 1.0
    total_frameworks: int
    total_requirements: int
    requirements_satisfied: int
    requirements_partial: int
    requirements_not_satisfied: int
    active_exceptions: int
    expired_exceptions: int
    active_remediations: int
    stale_evidence_count: int
    last_assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
