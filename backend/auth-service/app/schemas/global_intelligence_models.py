"""
TruthShield X — Global Threat Intelligence Fusion Models (Phase 27).

Strictly typed Pydantic models for Intelligence Sources, Threat Intelligence Records,
Campaign Clusters, Temporal Graphs, Emerging Threat Signals, Threat Forecasts,
Early Warnings, Defensive Hypotheses, Conflicts, and Feed Health.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 27)
# ============================================================================

SourceTypeLiteral = Literal[
    "INTERNAL",
    "PARTNER",
    "PUBLIC",
    "COMMERCIAL",
    "GOVERNMENT",
    "COMMUNITY",
    "SENSOR",
    "SOC",
    "INCIDENT",
    "USER_REPORTED",
]

IntelligenceTypeLiteral = Literal[
    "IOC",
    "IOA",
    "TTP",
    "VULNERABILITY",
    "MALWARE",
    "PHISHING",
    "CAMPAIGN",
    "THREAT_ACTOR",
    "INFRASTRUCTURE",
    "DOMAIN",
    "IP",
    "URL",
    "FILE_HASH",
    "CERTIFICATE",
    "IDENTITY",
    "ATTACK_PATTERN",
    "SECURITY_ADVISORY",
    "INCIDENT_SIGNAL",
]

ClaimStatusLiteral = Literal[
    "OBSERVED",
    "REPORTED",
    "CORRELATED",
    "INFERRED",
    "FORECAST",
    "SIMULATED",
    "CONFLICTING",
    "STALE",
    "EXPIRED",
    "INSUFFICIENT_EVIDENCE",
    "NOT_VERIFIED",
]

CampaignEvolutionLiteral = Literal[
    "NEW",
    "EXPANDING",
    "STABLE",
    "DECLINING",
    "UNKNOWN",
]

EarlyWarningSeverityLiteral = Literal[
    "INFORMATIONAL",
    "WATCH",
    "ELEVATED",
    "HIGH",
    "CRITICAL",
]

ForecastHorizonLiteral = Literal[
    "SHORT_TERM",
    "MEDIUM_TERM",
    "LONG_TERM",
]


# ============================================================================
# Intelligence Source & Feed Models
# ============================================================================

class IntelligenceSourceDTO(BaseModel):
    source_id: str = Field(default_factory=lambda: f"src_{uuid.uuid4().hex[:8]}")
    name: str = "Global Cyber Threat Exchange Feed"
    type: SourceTypeLiteral = "COMMERCIAL"
    source_reliability: float = 0.95
    information_reliability: float = 0.92
    freshness_status: Literal["FRESH", "AGING", "STALE", "EXPIRED"] = "FRESH"
    provenance_chain: List[str] = Field(default_factory=lambda: ["INGESTION_GATEWAY_V1"])
    trust_level: Literal["HIGH", "MEDIUM", "LOW", "UNTRUSTED"] = "HIGH"
    tenant_scope: str = "default_tenant"
    status: Literal["ACTIVE", "QUARANTINED", "DISABLED"] = "ACTIVE"
    last_synced_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ThreatIntelligenceRecordDTO(BaseModel):
    intelligence_id: str = Field(default_factory=lambda: f"intel_{uuid.uuid4().hex[:8]}")
    source_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    published_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    valid_from: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    valid_until: Optional[str] = None
    type: IntelligenceTypeLiteral = "IOC"
    indicator: str = "malicious-c2-domain.truthshield.internal"
    entity: Optional[str] = "DarkStorm C2 Infrastructure"
    behavior: Optional[str] = "DNS tunneling & reflective DLL loading"
    campaign_id: Optional[str] = "cmp_darkstorm_2026"
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"] = "HIGH"
    confidence_score: float = 0.94
    provenance: List[Dict[str, Any]] = Field(default_factory=list)
    evidence_hashes: List[str] = Field(default_factory=list)
    tenant_scope: str = "default_tenant"
    claim_status: ClaimStatusLiteral = "REPORTED"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Threat Campaign & Temporal Correlation Models
# ============================================================================

class ThreatCampaignDTO(BaseModel):
    campaign_id: str = Field(default_factory=lambda: f"cmp_{uuid.uuid4().hex[:8]}")
    name: str = "DarkStorm Global Supply-Chain Infiltration"
    confidence_score: float = 0.92
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    indicators: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=lambda: ["T1078", "T1055", "T1021"])
    infrastructure: List[str] = Field(default_factory=list)
    affected_sectors: List[str] = Field(default_factory=lambda: ["FINANCE", "DEFENSE", "CLOUD_INFRASTRUCTURE"])
    affected_assets: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    source_count: int = 4
    evolution_status: CampaignEvolutionLiteral = "EXPANDING"
    status: Literal["ACTIVE", "MONITORED", "CONTAINED", "ARCHIVED"] = "ACTIVE"

    model_config = ConfigDict(frozen=True)


class ThreatForecastDTO(BaseModel):
    forecast_id: str = Field(default_factory=lambda: f"fcst_{uuid.uuid4().hex[:8]}")
    subject: str = "DarkStorm Campaign Lateral Movement Velocity"
    horizon: ForecastHorizonLiteral = "SHORT_TERM"
    prediction: str = "Projected 40% increase in API credential stuffing across finance sector within 72 hours."
    confidence_score: float = 0.88
    evidence: List[str] = Field(default_factory=list)
    methodology: str = "ARIMA Time-Series on NetFlow Velocity + Attacker Infrastructure Clustering"
    assumptions: List[str] = Field(default_factory=lambda: ["C2 network topology remains un-isolated by tier-1 upstream ISPs"])
    limitations: List[str] = Field(default_factory=lambda: ["Forecast depends on dark web credential leak velocity"])
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiry: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    calibration_status: Literal["CALIBRATED", "UNCALIBRATED", "FORECAST_NOT_SUPPORTED"] = "CALIBRATED"

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Early Warning, Hypothesis & Conflict Models
# ============================================================================

class EarlyWarningSignalDTO(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"ew_{uuid.uuid4().hex[:8]}")
    threat_name: str = "DarkStorm Rapid C2 Expansion"
    severity: EarlyWarningSeverityLiteral = "HIGH"
    velocity_score: float = 0.85
    novelty_score: float = 0.78
    affected_assets: List[str] = Field(default_factory=list)
    recommended_action: str = "Pre-position rate-limiting Sigma rules on edge API gateways and simulate in Digital Twin."
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class DefensiveHypothesisDTO(BaseModel):
    hypothesis_id: str = Field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    threat_id: str
    hypothesis_statement: str = "If rate-limiting and MFA step-up are enforced, DarkStorm initial credential stuffing containment improves by 85%."
    testable_criteria: str = "Simulated credential stuffing containment time drops below 30s in Digital Twin Sandbox."
    digital_twin_scenario_id: Optional[str] = "scen_phishing_lateral_movement"
    recommended_validation: str = "Phase 26 Digital Twin Simulation -> Phase 24 Control Verification"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class IntelligenceConflictDTO(BaseModel):
    conflict_id: str = Field(default_factory=lambda: f"cnf_{uuid.uuid4().hex[:8]}")
    entity_id: str = "c2_domain_dispute"
    contradicting_sources: List[str] = Field(default_factory=lambda: ["src_commercial_feed_a", "src_partner_telemetry"])
    conflicting_claims: List[str] = Field(default_factory=lambda: ["Reported as ACTIVE C2", "Reported as BENIGN CDN SINKHOLE"])
    resolution_status: Literal["PRESERVED_CONFLICT", "RESOLVED"] = "PRESERVED_CONFLICT"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
