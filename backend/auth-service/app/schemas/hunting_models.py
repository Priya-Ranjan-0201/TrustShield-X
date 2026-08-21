"""
TruthShield X — Phase 11 Autonomous Threat Hunting, Attack Path Reasoning & Predictive Defense Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


HypothesisTypeLiteral = Literal[
    "CAMPAIGN_EXPANSION",
    "ASSET_COMPROMISE",
    "IMPERSONATION",
    "PHISHING_CAMPAIGN",
    "MALWARE_CAMPAIGN",
    "INFRASTRUCTURE_REUSE",
    "IDENTITY_ABUSE",
    "PAYMENT_FRAUD",
    "TRUST_DEGRADATION",
    "EXPOSURE_ESCALATION",
    "ANOMALOUS_BEHAVIOR",
    "SUPPLY_CHAIN_RISK",
    "THIRD_PARTY_RISK",
    "UNKNOWN_THREAT",
]

HypothesisStatusLiteral = Literal[
    "DRAFT",
    "ACTIVE",
    "INVESTIGATING",
    "SUPPORTED",
    "WEAKLY_SUPPORTED",
    "REFUTED",
    "INCONCLUSIVE",
    "CLOSED",
]

HuntConclusionLiteral = Literal[
    "THREAT_CONFIRMED",
    "THREAT_SUPPORTED",
    "SUSPICIOUS",
    "INCONCLUSIVE",
    "BENIGN",
    "FALSE_POSITIVE",
    "INSUFFICIENT_EVIDENCE",
]

WarningLevelLiteral = Literal[
    "INFORMATIONAL",
    "WATCH",
    "ELEVATED",
    "HIGH",
    "CRITICAL",
]

PredictionHorizonLiteral = Literal[
    "SHORT_TERM",   # 1 - 7 days
    "MEDIUM_TERM",  # 8 - 30 days
    "LONG_TERM",    # 31 - 90 days
]


class ThreatHuntHypothesisDTO(BaseModel):
    hypothesis_id: str
    tenant_id: str = "default_tenant"
    title: str
    description: str
    hypothesis_type: HypothesisTypeLiteral
    status: HypothesisStatusLiteral = "ACTIVE"
    priority: str = "HIGH"
    confidence: float = 0.75
    created_by: str = "AI_THREAT_HUNTER_V11"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_count: int = 0
    supporting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    counter_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    alternative_hypotheses: List[str] = Field(default_factory=list)
    conclusion: Optional[HuntConclusionLiteral] = None
    target_assets: List[str] = Field(default_factory=list)


class AttackPathEdgeDTO(BaseModel):
    edge_id: str
    source_node: str
    target_node: str
    relationship: str
    node_type: Literal["ENTRY_POINT", "EXPOSURE", "ENTITY", "INFRASTRUCTURE", "CAMPAIGN", "TARGET", "POTENTIAL_IMPACT"]
    classification: Literal["OBSERVED", "POTENTIAL", "INFERRED", "PREDICTED"]
    confidence: float
    provenance: Dict[str, Any] = Field(default_factory=dict)


class AttackPathGraphDTO(BaseModel):
    path_id: str
    title: str
    target_asset: str
    edges: List[AttackPathEdgeDTO]
    overall_confidence: float
    blast_radius_classification: Literal["VERIFIED_AFFECTED", "LIKELY_AFFECTED", "POTENTIALLY_AFFECTED", "NOT_SUPPORTED"]
    alternative_paths_count: int = 1
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EarlyWarningDTO(BaseModel):
    warning_id: str
    tenant_id: str = "default_tenant"
    title: str
    warning_level: WarningLevelLiteral
    confidence: float
    contributing_signals: List[str]
    affected_assets: List[str]
    predicted_impact: str
    recommended_investigation: str
    issued_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityPredictionDTO(BaseModel):
    prediction_id: str
    tenant_id: str = "default_tenant"
    target_subject: str
    prediction_type: str  # EXPOSURE_SPIKE, CAMPAIGN_EXPANSION, TRUST_DEGRADATION, INFRASTRUCTURE_REUSE
    horizon: PredictionHorizonLiteral
    predicted_probability: float
    confidence: float
    assumptions: List[str]
    supporting_evidence: List[Dict[str, Any]]
    model_version: str = "TruthShield-Predict-v11.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    actual_outcome: Optional[Literal["CORRECT", "PARTIALLY_CORRECT", "INCORRECT", "UNRESOLVED"]] = "UNRESOLVED"
    outcome_observed_at: Optional[str] = None


class ThreatHuntResultDTO(BaseModel):
    result_id: str
    hypothesis_id: str
    conclusion: HuntConclusionLiteral
    confidence: float
    supporting_evidence: List[Dict[str, Any]]
    counter_evidence: List[Dict[str, Any]]
    affected_assets: List[str]
    related_campaigns: List[str]
    attack_paths: List[AttackPathGraphDTO] = Field(default_factory=list)
    recommendations: List[str]
    limitations: List[str]
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HuntBudgetConfigDTO(BaseModel):
    max_duration_seconds: int = 60
    max_records_to_scan: int = 1000
    max_graph_expansions: int = 50
    memory_limit_mb: int = 256
