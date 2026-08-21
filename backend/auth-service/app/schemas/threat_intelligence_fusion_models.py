"""
TruthShield X — Phase 33 Threat Intelligence Fusion & Predictive Control Plane Models.

Pydantic DTOs for multi-source correlation, actor/campaign profiles, IOC/IOA/IOB,
quality scorecards, graph nodes/edges, forecasts, early-warning signals, and dissemination.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class IntelligenceRecordDTO(BaseModel):
    intelligence_id: str
    source: str
    source_type: str  # GOVERNMENT, CERT, ISAC, VENDOR, COMMERCIAL, OPEN_SOURCE, INTERNAL, SENSOR, INCIDENT, COMMUNITY, MANUAL, PARTNER
    source_reliability: str = "B"  # A-F Admiralty Scale
    information_credibility: str = "2"  # 1-6 Admiralty Scale
    collection_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    publication_time: Optional[str] = None
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    content_hash: str
    classification: str = "INTERNAL"  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED, HIGHLY_RESTRICTED
    tenant_scope: str = "GLOBAL"  # GLOBAL, ORGANIZATION, TENANT, PRIVATE
    confidence: float = 0.85
    status: str = "INGESTED"  # INGESTED, NORMALIZED, VALIDATED, ENRICHED, CORRELATED, ASSESSED, VERIFIED, DISPUTED, STALE, RETIRED
    raw_payload: Dict[str, Any] = Field(default_factory=dict)
    provenance: List[str] = Field(default_factory=list)


class IntelligenceSourceDTO(BaseModel):
    source_id: str
    source_name: str
    source_type: str
    provider: str
    reliability: str = "A"
    collection_method: str = "API"  # STIX, TAXII, JSON, CSV, RSS, API, WEBHOOK, MANUAL
    authentication: str = "API_KEY"
    last_success: Optional[str] = None
    last_failure: Optional[str] = None
    freshness: str = "FRESH"  # FRESH, AGING, STALE, UNKNOWN
    supported_formats: List[str] = Field(default_factory=lambda: ["JSON", "STIX2.1"])
    classification: str = "INTERNAL"
    approval_status: str = "APPROVED"  # APPROVED, PENDING, SUSPENDED, QUARANTINED
    error_count: int = 0
    is_compromised: bool = False


class IndicatorDTO(BaseModel):
    indicator_id: str
    indicator_type: str  # IPv4, IPv6, DOMAIN, URL, HASH, EMAIL, FILE, CERTIFICATE, ASSET, USER_AGENT, PROCESS, REGISTRY_KEY, MUTEX, PACKAGE, CVE, CPE
    raw_value: str
    normalized_value: str
    canonical_hash: str
    status: str = "OBSERVED"  # OBSERVED, REPORTED, CORRELATED, VERIFIED, ACTIVE, EXPIRED, RETIRED, FALSE_POSITIVE
    confidence: float = 0.80
    source_count: int = 1
    sources: List[str] = Field(default_factory=list)
    related_campaigns: List[str] = Field(default_factory=list)
    related_actors: List[str] = Field(default_factory=list)
    related_malware: List[str] = Field(default_factory=list)
    related_techniques: List[str] = Field(default_factory=list)
    affected_assets: List[str] = Field(default_factory=list)
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    behavior_type: Optional[str] = None  # IOA or IOB behavioral pattern if applicable


class ThreatCampaignDTO(BaseModel):
    campaign_id: str
    name: str
    description: str
    first_seen: str
    last_seen: str
    indicators: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)  # MITRE ATT&CK techniques
    malware: List[str] = Field(default_factory=list)
    infrastructure: List[str] = Field(default_factory=list)
    affected_sectors: List[str] = Field(default_factory=list)
    affected_regions: List[str] = Field(default_factory=list)
    related_actors: List[str] = Field(default_factory=list)
    confidence: float = 0.85
    evidence: List[str] = Field(default_factory=list)
    status: str = "ACTIVE"  # ACTIVE, DORMANT, HISTORICAL, ATTRIBUTED


class ThreatActorProfileDTO(BaseModel):
    actor_id: str
    name: str
    aliases: List[str] = Field(default_factory=list)
    associated_campaigns: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    infrastructure: List[str] = Field(default_factory=list)
    malware: List[str] = Field(default_factory=list)
    targeted_sectors: List[str] = Field(default_factory=list)
    targeted_regions: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)
    confidence: float = 0.75
    attribution_status: str = "ASSESSED"  # UNATTRIBUTED, SUSPECTED, ASSESSED, CORROBORATED, VERIFIED, DISPUTED


class MalwareProfileDTO(BaseModel):
    malware_id: str
    malware_family: str
    aliases: List[str] = Field(default_factory=list)
    hashes: List[str] = Field(default_factory=list)
    infrastructure: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    campaigns: List[str] = Field(default_factory=list)
    detection_rules: List[str] = Field(default_factory=list)
    confidence: float = 0.90


class VulnerabilityIntelligenceDTO(BaseModel):
    cve_id: str
    cvss_score: float = 0.0
    affected_products: List[str] = Field(default_factory=list)
    exploitation_status: str = "VULNERABLE"  # VULNERABLE, EXPLOITABLE, ACTIVELY_EXPLOITED
    vendor_advisories: List[str] = Field(default_factory=list)
    remediation: Optional[str] = None
    asset_exposure_count: int = 0
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence: List[str] = Field(default_factory=list)


class IntelligenceQualityScorecardDTO(BaseModel):
    source_reliability: str = "A"
    information_credibility: str = "1"
    freshness_score: float = 0.95
    corroboration_count: int = 3
    context_completeness: float = 0.88
    provenance_verified: bool = True
    overall_quality_assessment: str = "HIGH_QUALITY_GROUNDED"


class ThreatForecastDTO(BaseModel):
    forecast_id: str
    predicted_threat: str
    forecast_horizon: str  # 24_HOURS, 7_DAYS, 30_DAYS, 90_DAYS
    predicted_probability: float
    state: str = "FORECAST"  # SIGNAL, FORECAST, HIGH_CONFIDENCE_FORECAST, VERIFIED_EVENT, EXPIRED_FORECAST, INVALIDATED_FORECAST
    evidence: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    uncertainty: str = "LOW"
    calibration_brier_score: Optional[float] = 0.08
    outcome: Optional[str] = None


class ThreatEarlyWarningDTO(BaseModel):
    warning_id: str
    reason: str
    evidence: List[str] = Field(default_factory=list)
    urgency: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    affected_assets: List[str] = Field(default_factory=list)
    affected_sectors: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    confidence: float = 0.90
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceConflictDTO(BaseModel):
    conflict_id: str
    indicator_or_entity: str
    claim_a: str
    source_a: str
    claim_b: str
    source_b: str
    status: str = "INTELLIGENCE_CONFLICT"
    resolution_notes: Optional[str] = None
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntelligenceSnapshotDTO(BaseModel):
    snapshot_id: str
    snapshot_type: str  # CAMPAIGN, ACTOR, INDICATOR, LANDSCAPE
    entity_id: str
    content_state: Dict[str, Any]
    snapshot_hash: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DisseminationRecordDTO(BaseModel):
    dissemination_id: str
    product_type: str  # IOC_BUNDLE, THREAT_ALERT, CAMPAIGN_BRIEF, ACTOR_PROFILE, VULNERABILITY_ALERT, EARLY_WARNING, FORECAST, CANDIDATE_DETECTION
    recipient: str
    classification: str
    policy_verdict: str  # PERMITTED, BLOCKED
    reason: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
