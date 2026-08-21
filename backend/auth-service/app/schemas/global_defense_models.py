"""
TruthShield X — Global Cyber Defense Coordination Models (Phase 28).

Strictly typed Pydantic models for Defense Coordination Cases, Defense Networks,
Intelligence Sharing Policies, Sanitized Records, Defensive Knowledge Records,
Coordinated Response Plans, Coordination SLAs, and Global Defense Scorecards.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 28)
# ============================================================================

CoordinationStateLiteral = Literal[
    "DISCOVERED",
    "ASSESSED",
    "CANDIDATE",
    "SHARING_REVIEW",
    "SANITIZED",
    "PROPOSED",
    "APPROVAL_REQUIRED",
    "APPROVED",
    "ACTIVE",
    "CONTAINED",
    "RECOVERING",
    "VERIFIED",
    "CLOSED",
    "REJECTED",
    "BLOCKED",
]

DataClassificationLiteral = Literal[
    "PUBLIC",
    "INTERNAL",
    "CONFIDENTIAL",
    "RESTRICTED",
    "HIGHLY_RESTRICTED",
]

TrustLevelLiteral = Literal[
    "UNTRUSTED",
    "OBSERVED",
    "VERIFIED",
    "TRUSTED",
    "RESTRICTED",
]

ClaimStatusLiteral = Literal[
    "OBSERVED",
    "REPORTED",
    "VERIFIED",
    "CORRELATED",
    "PROPOSED",
    "APPROVED",
    "ACTIVE",
    "CONTAINED",
    "RECOVERING",
    "VERIFIED_COMPLETE",
    "CONFLICTING",
    "BLOCKED",
    "NOT_VERIFIED",
]


# ============================================================================
# Defense Coordination Case & Network Models
# ============================================================================

class DefenseCoordinationCaseDTO(BaseModel):
    coordination_id: str = Field(default_factory=lambda: f"coord_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    threat_id: str = "cmp_darkstorm_2026"
    campaign_id: str = "cmp_darkstorm_2026"
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    objective: str = "Coordinated API Gateway Rate-Limiting & C2 Ingress Quarantine across Finance Peers"
    participating_entities: List[str] = Field(default_factory=lambda: ["tenant_finance_alpha", "tenant_cloud_beta"])
    sharing_policy_id: str = "pol_strict_sanitized_share"
    classification: DataClassificationLiteral = "CONFIDENTIAL"
    evidence: List[str] = Field(default_factory=lambda: ["Multi-tenant indicator intersection", "Digital Twin Simulation Verification"])
    proposed_actions: List[Dict[str, Any]] = Field(default_factory=list)
    approval_status: Literal["PENDING", "APPROVED", "REJECTED"] = "APPROVED"
    execution_status: CoordinationStateLiteral = "ACTIVE"
    verification_status: Literal["VERIFIED", "NOT_VERIFIED", "FAILED"] = "VERIFIED"
    outcome: Optional[str] = "DarkStorm C2 lateral propagation intercepted across 100% of participating peers."
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class DefenseNetworkDTO(BaseModel):
    network_id: str = Field(default_factory=lambda: f"net_{uuid.uuid4().hex[:8]}")
    name: str = "Global Financial ISAC Cyber Defense Network"
    participants: List[str] = Field(default_factory=lambda: ["tenant_finance_alpha", "tenant_cloud_beta", "cert_eu_exchange"])
    scope: str = "CROSS_ORGANIZATION_THREAT_SHARING"
    trust_level: TrustLevelLiteral = "VERIFIED"
    expiration: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: Literal["ACTIVE", "EXPIRED", "REVOKED"] = "ACTIVE"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Sharing Policy & Sanitization Models
# ============================================================================

class IntelligenceSharingPolicyDTO(BaseModel):
    policy_id: str = Field(default_factory=lambda: f"pol_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    allowed_classifications: List[DataClassificationLiteral] = Field(default_factory=lambda: ["PUBLIC", "INTERNAL", "CONFIDENTIAL"])
    auto_sanitize: bool = True
    requires_four_eyes: bool = True
    sharing_purposes: List[str] = Field(default_factory=lambda: ["THREAT_DEFENSE", "INCIDENT_MITIGATION"])
    recipients: List[str] = Field(default_factory=lambda: ["ALL_AUTHORIZED_NETWORK_MEMBERS"])

    model_config = ConfigDict(frozen=True)


class SanitizedRecordDTO(BaseModel):
    record_id: str = Field(default_factory=lambda: f"sanrec_{uuid.uuid4().hex[:8]}")
    original_classification: DataClassificationLiteral = "RESTRICTED"
    redacted_fields_count: int = 4
    sanitized_payload: Dict[str, Any] = Field(default_factory=dict)
    sanitization_status: Literal["SANITIZED", "SANITIZATION_REQUIRED", "SHARING_BLOCKED"] = "SANITIZED"
    verified_clean: bool = True
    sanitized_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Defensive Knowledge, Response Plans & SLAs
# ============================================================================

class DefensiveKnowledgeRecordDTO(BaseModel):
    knowledge_id: str = Field(default_factory=lambda: f"dknow_{uuid.uuid4().hex[:8]}")
    problem: str = "DarkStorm C2 DNS Tunneling via Ephemeral Port Bursts"
    evidence: List[str] = Field(default_factory=lambda: ["PCAP DNS payload entropy", "NetFlow burst spikes"])
    defensive_technique: str = "Deploy DNS Entropy Detection Sigma Rule & Dynamic Rate-Limiter"
    validation_result: str = "Verified 85% Containment in Phase 26 Digital Twin Lab"
    environment: str = "LINUX_KUBERNETES_CONTAINERS"
    compatibility: List[str] = Field(default_factory=lambda: ["CORE_DNS", "NGINX_INGRESS", "FASTAPI_GW"])
    source_tenant_scope: str = "default_tenant"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class CoordinatedResponsePlanDTO(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"plan_{uuid.uuid4().hex[:8]}")
    coordination_id: str
    objective: str = "Synchronized Host Quarantine & Credential Revocation"
    participants: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    approvals: List[str] = Field(default_factory=lambda: ["CISO_APPROVAL_AUTH", "SOC_LEAD_APPROVAL_AUTH"])
    timeline: Dict[str, str] = Field(default_factory=dict)
    rollback_procedure: str = "Re-enable quarantined routes via emergency automated token"
    verification_gate: str = "Phase 24 Control Re-Verification"

    model_config = ConfigDict(frozen=True)


class CoordinationSLADTO(BaseModel):
    sla_id: str = Field(default_factory=lambda: f"sla_{uuid.uuid4().hex[:8]}")
    coordination_id: str
    notification_sla_seconds: float = 300.0
    ack_sla_seconds: float = 600.0
    response_sla_seconds: float = 1800.0
    recovery_sla_seconds: float = 3600.0
    is_compliant: bool = True

    model_config = ConfigDict(frozen=True)


class GlobalDefenseScorecardDTO(BaseModel):
    scorecard_id: str = Field(default_factory=lambda: f"scard_{uuid.uuid4().hex[:8]}")
    threat_readiness_score: float = 0.94
    detection_readiness_score: float = 0.96
    response_readiness_score: float = 0.92
    recovery_readiness_score: float = 0.95
    intelligence_quality_score: float = 0.94
    coordination_readiness_score: float = 0.90
    control_effectiveness_score: float = 0.95
    information_sharing_readiness_score: float = 0.92
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
