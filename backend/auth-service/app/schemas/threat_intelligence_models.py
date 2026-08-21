"""Pydantic v2 DTO Schemas for Enterprise Threat Intelligence & External Indicator Correlation Engine (Phase 3.9 Part 1A.23).

Strictly typed DTOs for threat indicators, sources, feeds, matches, relationships, entities, conflicts,
evidence, behavior correlations, dataflow correlations, evidence cards, summaries, threat graphs, YARA matches, STIX objects, TAXII collections, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ThreatIndicatorDTO(BaseModel):
    indicator_id: str
    indicator_type: str = "DOMAIN"  # APK_SHA256, APK_SHA1, APK_MD5, DEX_SHA256, NATIVE_LIBRARY_SHA256, FILE_SHA256, PACKAGE_NAME, APPLICATION_ID, SIGNING_CERTIFICATE_SHA256, SIGNING_CERTIFICATE_SHA1, CERTIFICATE_SERIAL, CERTIFICATE_FINGERPRINT, DOMAIN, SUBDOMAIN, URL, IPV4, IPV6, PORT, NETWORK_ENDPOINT, TLS_CERTIFICATE, MALWARE_FAMILY, THREAT_ACTOR, CAMPAIGN, YARA_INDICATOR, STIX_INDICATOR, TAXII_OBJECT
    normalized_value: str
    display_value: str
    value_hash: str
    source_module: str
    source_location: str
    resolution_status: str = "RESOLVED"
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatSourceDTO(BaseModel):
    source_id: str
    provider: str
    source_type: str = "OFFLINE_FEED"
    reliability: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, UNKNOWN
    version: str = "1.0"
    status: str = "ACTIVE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatFeedDTO(BaseModel):
    feed_id: str
    feed_name: str
    provider: str
    version: str
    record_count: int = 0
    freshness_state: str = "CURRENT"  # CURRENT, RECENT, STALE, EXPIRED, UNKNOWN

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatMatchDTO(BaseModel):
    match_id: str
    indicator_id: str
    source_id: str
    match_type: str = "EXACT_MATCH"  # EXACT_MATCH, DOMAIN_MATCH, URL_MATCH, PATH_MATCH, CERTIFICATE_MATCH, HASH_MATCH, PACKAGE_MATCH, INFRASTRUCTURE_MATCH, YARA_MATCH, STIX_MATCH, RELATIONSHIP_MATCH, SIMILARITY_MATCH, PARTIAL_MATCH, NO_MATCH, UNKNOWN
    reputation: str = "SUSPICIOUS_REPORTED"  # MALICIOUS_REPORTED, PHISHING_REPORTED, SUSPICIOUS_REPORTED, CLEAN_REPORTED, UNKNOWN, CONFLICTED
    confidence: str = "HIGH"
    freshness_state: str = "CURRENT"
    provenance: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatRelationshipDTO(BaseModel):
    source_entity_id: str
    target_entity_id: str
    relationship: str = "ASSOCIATED_WITH"
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatEntityDTO(BaseModel):
    entity_id: str
    entity_type: str = "INDICATOR"
    name: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatConflictDTO(BaseModel):
    conflict_id: str
    indicator_value: str
    source_a_claim: str
    source_b_claim: str
    resolution_status: str = "CONFLICTED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatEvidenceDTO(BaseModel):
    evidence_id: str
    indicator_id: str
    matched_rule_or_feed: str
    provenance: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatBehaviorCorrelationDTO(BaseModel):
    correlation_id: str
    behavior_type: str
    indicator_value: str
    threat_claim: str
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatDataflowCorrelationDTO(BaseModel):
    correlation_id: str
    dataflow_path_id: str
    endpoint_url: str
    threat_claim: str
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatCardDTO(BaseModel):
    card_id: str
    title: str
    category: str
    observed_indicator: str
    threat_claim: str
    confidence: str = "HIGH"
    freshness: str = "CURRENT"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatSummaryDTO(BaseModel):
    title: str
    summary_text: str
    matches_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class YaraMatchDTO(BaseModel):
    rule_name: str
    rule_namespace: str = "default"
    matched_file: str
    offset: int = 0
    match_confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StixObjectDTO(BaseModel):
    object_id: str
    object_type: str = "indicator"
    name: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class TaxiiCollectionDTO(BaseModel):
    collection_id: str
    title: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatMetricsDTO(BaseModel):
    indicators_processed: int = 0
    matches_count: int = 0
    conflicts_count: int = 0
    expired_indicators_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThreatIntelligenceResultDTO(BaseModel):
    indicators: List[ThreatIndicatorDTO] = Field(default_factory=list)
    sources: List[ThreatSourceDTO] = Field(default_factory=list)
    feeds: List[ThreatFeedDTO] = Field(default_factory=list)
    matches: List[ThreatMatchDTO] = Field(default_factory=list)
    relationships: List[ThreatRelationshipDTO] = Field(default_factory=list)
    entities: List[ThreatEntityDTO] = Field(default_factory=list)
    conflicts: List[ThreatConflictDTO] = Field(default_factory=list)
    evidence: List[ThreatEvidenceDTO] = Field(default_factory=list)
    behavior_correlations: List[ThreatBehaviorCorrelationDTO] = Field(default_factory=list)
    dataflow_correlations: List[ThreatDataflowCorrelationDTO] = Field(default_factory=list)
    cards: List[ThreatCardDTO] = Field(default_factory=list)
    summaries: List[ThreatSummaryDTO] = Field(default_factory=list)
    threat_graph: ThreatGraphDTO = Field(default_factory=ThreatGraphDTO)
    yara_matches: List[YaraMatchDTO] = Field(default_factory=list)
    stix_objects: List[StixObjectDTO] = Field(default_factory=list)
    taxii_collections: List[TaxiiCollectionDTO] = Field(default_factory=list)
    metrics: ThreatMetricsDTO = Field(default_factory=ThreatMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
