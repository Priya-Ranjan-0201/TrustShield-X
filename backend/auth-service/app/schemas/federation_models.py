"""
TruthShield X — Phase 10 Federated Digital Trust Graph & Threat Intelligence Exchange Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


IntelligenceTypeLiteral = Literal[
    "DOMAIN",
    "URL",
    "IP",
    "CERTIFICATE",
    "HASH",
    "APK",
    "PACKAGE",
    "PHONE",
    "UPI_IDENTIFIER",
    "EMAIL",
    "CAMPAIGN",
    "ATTACK_PATTERN",
    "INFRASTRUCTURE",
    "BEHAVIOR",
    "THREAT_SIGNAL",
    "DIGITAL_TRUST_EVENT",
]

SharingScopeLiteral = Literal[
    "PRIVATE",
    "INTERNAL",
    "TRUSTED_PARTNER",
    "COMMUNITY",
    "GLOBAL",
]

VerificationStatusLiteral = Literal[
    "UNVERIFIED",
    "OBSERVED",
    "CORROBORATED",
    "VERIFIED",
    "DISPUTED",
    "EXPIRED",
    "REVOKED",
]

SharingDecisionLiteral = Literal[
    "SHARE",
    "SHARE_REDACTED",
    "SHARE_AGGREGATED",
    "SHARE_INTERNAL_ONLY",
    "REJECT",
]

ConflictStateLiteral = Literal[
    "UNRESOLVED",
    "UNDER_REVIEW",
    "RESOLVED_MALICIOUS",
    "RESOLVED_BENIGN",
    "RESOLVED_CONTEXTUAL",
    "INCONCLUSIVE",
]

QuarantineStatusLiteral = Literal[
    "QUARANTINED",
    "UNDER_REVIEW",
    "APPROVED",
    "REJECTED",
    "RELEASED",
]


class FederatedIntelligenceObjectDTO(BaseModel):
    intelligence_id: str
    intelligence_type: IntelligenceTypeLiteral
    canonical_identifier: str
    tenant_scope: str = "default_tenant"
    sharing_scope: SharingScopeLiteral = "PRIVATE"
    classification: str = "CONFIDENTIAL"
    confidence: float = 0.85
    verification_status: VerificationStatusLiteral = "OBSERVED"
    provenance: Dict[str, Any] = Field(default_factory=dict)
    source_type: str = "INTERNAL_OBSERVATION"
    source_reliability: float = 0.90
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiration: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    redacted_attributes: List[str] = Field(default_factory=list)


class SharingPolicyDecisionDTO(BaseModel):
    policy_id: str
    decision: SharingDecisionLiteral
    reason: str
    evaluated_attributes: Dict[str, Any]
    detected_pii: List[str] = Field(default_factory=list)
    detected_secrets: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceConflictDTO(BaseModel):
    conflict_id: str
    canonical_identifier: str
    conflicting_claims: List[Dict[str, Any]]  # List of {source, claim, confidence, timestamp}
    resolution_state: ConflictStateLiteral = "UNRESOLVED"
    resolution_notes: Optional[str] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceSourceReputationDTO(BaseModel):
    source_id: str
    source_name: str
    source_type: str  # INTERNAL, PARTNER, PUBLIC_FEED, STIX_TAXII
    reliability_score: float  # 0.0 - 1.0
    total_indicators_submitted: int = 0
    verified_indicators_count: int = 0
    false_positives_count: int = 0
    revoked_count: int = 0
    conflicts_count: int = 0
    status: str = "ACTIVE"  # ACTIVE, DEGRADED, SUSPENDED, QUARANTINED
    last_sync: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceQuarantineEntryDTO(BaseModel):
    quarantine_id: str
    source_id: str
    reason: str
    affected_indicators: List[str] = Field(default_factory=list)
    status: QuarantineStatusLiteral = "QUARANTINED"
    risk_level: str = "HIGH"
    quarantined_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None


class ActorHypothesisDTO(BaseModel):
    hypothesis_id: str
    actor_label: str
    confidence: float
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    counter_evidence_ids: List[str] = Field(default_factory=list)
    alternative_hypotheses: List[str] = Field(default_factory=list)
    status: str = "HYPOTHESIS_UNCONFIRMED"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceFeedbackDTO(BaseModel):
    feedback_id: str
    intelligence_id: str
    consumer_tenant_id: str
    feedback_type: Literal["USEFUL", "INACCURATE", "OUTDATED", "MALICIOUS", "DUPLICATE"]
    notes: Optional[str] = None
    submitted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceExportResultDTO(BaseModel):
    export_id: str
    export_scope: SharingScopeLiteral
    exporter_tenant_id: str
    exported_count: int
    data: List[Dict[str, Any]]
    policy_decision: str
    exported_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
