"""
TruthShield X — Phase 8 Continuous Digital Trust Monitoring & Exposure Management Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


AssetTypeLiteral = Literal[
    "DOMAIN",
    "SUBDOMAIN",
    "URL",
    "IP_ADDRESS",
    "CERTIFICATE",
    "EMAIL_DOMAIN",
    "EMAIL_ACCOUNT",
    "PHONE_NUMBER",
    "UPI_IDENTIFIER",
    "API_ENDPOINT",
    "WEB_APPLICATION",
    "MOBILE_APPLICATION",
    "APK",
    "PACKAGE",
    "CLOUD_ASSET",
    "STORAGE_ASSET",
    "DNS_RECORD",
    "NETWORK_SERVICE",
    "DIGITAL_IDENTITY",
    "SOCIAL_ACCOUNT",
    "BRAND",
    "ORGANIZATION",
    "DEVICE",
    "THIRD_PARTY_SERVICE",
    "CRYPTO_IDENTIFIER",
]

OwnershipStatusLiteral = Literal[
    "VERIFIED_OWNER",
    "CLAIMED_OWNER",
    "AUTHORIZED_MONITORING",
    "THIRD_PARTY",
    "UNKNOWN",
]

AssetCriticalityLiteral = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]

MonitoringStatusLiteral = Literal[
    "CONFIGURED",
    "SCHEDULED",
    "RUNNING",
    "COMPLETED",
    "FAILED",
    "RETRYING",
    "PAUSED",
    "DISABLED",
]

ChangeClassificationLiteral = Literal[
    "BENIGN",
    "EXPECTED",
    "INFORMATIONAL",
    "SUSPICIOUS",
    "HIGH_RISK",
    "CRITICAL",
]

ShadowAssetStatusLiteral = Literal[
    "POSSIBLE_SHADOW_ASSET",
    "PROBABLE_SHADOW_ASSET",
    "VERIFIED_UNDECLARED_ASSET",
    "UNKNOWN",
]

FindingLifecycleLiteral = Literal[
    "NEW",
    "TRIAGED",
    "INVESTIGATING",
    "ACKNOWLEDGED",
    "MITIGATING",
    "RESOLVED",
    "FALSE_POSITIVE",
    "ACCEPTED_RISK",
    "REOPENED",
]

SourceTypeLiteral = Literal[
    "PASSIVE",
    "AUTHORIZED_ACTIVE",
    "THIRD_PARTY_INTELLIGENCE",
    "INTERNAL",
]


class AssetDTO(BaseModel):
    asset_id: str
    asset_type: AssetTypeLiteral
    canonical_identifier: str
    display_identifier: str
    ownership_status: OwnershipStatusLiteral = "UNKNOWN"
    authorization_status: str = "PENDING_VERIFICATION"
    criticality: AssetCriticalityLiteral = "MEDIUM"
    tenant_id: str = "default_tenant"
    classification: str = "INTERNAL"
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    current_state: str = "ACTIVE"
    trust_score: float = 85.0
    risk_score: float = 15.0
    exposure_score: float = 20.0
    monitoring_status: MonitoringStatusLiteral = "CONFIGURED"
    monitoring_frequency: str = "HOURLY"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AssetBaselineDTO(BaseModel):
    baseline_id: str
    asset_id: str
    tenant_id: str = "default_tenant"
    version: int = 1
    dns_records: Dict[str, Any] = Field(default_factory=dict)
    tls_certificate: Dict[str, Any] = Field(default_factory=dict)
    http_headers: Dict[str, Any] = Field(default_factory=dict)
    exposed_ports: List[int] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    trust_score_baseline: float = 85.0
    risk_score_baseline: float = 15.0
    exposure_score_baseline: float = 20.0
    known_relationships: List[str] = Field(default_factory=list)
    established_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AssetObservationDTO(BaseModel):
    observation_id: str
    asset_id: str
    tenant_id: str = "default_tenant"
    source_type: SourceTypeLiteral = "PASSIVE"
    source_name: str
    observed_data: Dict[str, Any]
    confidence: float = 0.90
    observed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AssetChangeDTO(BaseModel):
    change_id: str
    asset_id: str
    tenant_id: str = "default_tenant"
    change_type: str
    classification: ChangeClassificationLiteral = "INFORMATIONAL"
    previous_state: Dict[str, Any]
    new_state: Dict[str, Any]
    evidence_id: str
    confidence: float = 0.95
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExposureFindingDTO(BaseModel):
    finding_id: str
    asset_id: str
    tenant_id: str = "default_tenant"
    title: str
    description: str
    severity: str = "MEDIUM"
    lifecycle_state: FindingLifecycleLiteral = "NEW"
    exposure_score: float
    risk_score: float
    trust_score: float
    evidence_ids: List[str] = Field(default_factory=list)
    campaign_ids: List[str] = Field(default_factory=list)
    change_id: Optional[str] = None
    recommended_action: str
    provenance: Dict[str, Any] = Field(default_factory=dict)
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CorrelatedExposureEventDTO(BaseModel):
    event_id: str
    tenant_id: str = "default_tenant"
    affected_assets: List[str]
    finding_ids: List[str]
    title: str
    summary: str
    severity: str
    aggregate_exposure_score: float
    projected_risk_score: float
    campaign_association: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ShadowAssetDTO(BaseModel):
    shadow_id: str
    canonical_identifier: str
    asset_type: AssetTypeLiteral
    shadow_status: ShadowAssetStatusLiteral = "POSSIBLE_SHADOW_ASSET"
    discovery_source: str
    confidence: float = 0.75
    related_brand_or_domain: str
    discovery_evidence: List[str] = Field(default_factory=list)
    tenant_id: str = "default_tenant"
    discovered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BrandImpersonationFindingDTO(BaseModel):
    impersonation_id: str
    target_brand: str
    suspect_identifier: str
    impersonation_type: str  # e.g., TYPOSQUAT_DOMAIN, FAKE_UPI, PHISHING_APK
    similarity_score: float
    risk_score: float
    confidence: float
    evidence: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = "default_tenant"
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AttackSurfaceSummaryDTO(BaseModel):
    tenant_id: str
    total_assets: int
    monitored_assets: int
    unmonitored_assets: int
    unknown_ownership_assets: int
    high_exposure_assets: int
    critical_exposure_assets: int
    active_findings_count: int
    shadow_assets_count: int
    brand_impersonations_count: int
    mean_exposure_score: float
    mean_trust_score: float
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
