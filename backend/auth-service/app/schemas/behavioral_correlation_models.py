"""Pydantic v2 DTO Schemas for Enterprise Behavioral Correlation & Multi-Source Intelligence Fusion Engine (Phase 3.9 Part 1A.22).

Strictly typed DTOs for evidence, entities, relationships, chains, findings, conflicts, summaries,
evidence cards, behavioral graphs, correlation graphs, third-party behaviors, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class CorrelationEvidenceDTO(BaseModel):
    evidence_id: str
    module: str
    entity_type: str = "API"
    entity_id: str
    class_name: str
    method_name: str
    instruction_offset: int = 0
    source_location: str
    rule_id: str
    evidence_type: str = "API_USAGE"
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"
    provenance: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorEntityDTO(BaseModel):
    entity_id: str
    entity_type: str = "CLASS"  # APK, DEX, CLASS, METHOD, API, PERMISSION, COMPONENT, INTENT, DOMAIN, IP, ENDPOINT, NETWORK_OPERATION, SOCKET, DATABASE, TABLE, COLUMN, FILE, STORAGE, PREFERENCE, CONTENT_PROVIDER, URI, CRYPTO_OPERATION, KEY_REFERENCE, CERTIFICATE, REFLECTION_TARGET, JNI_METHOD, SOURCE, SINK, DATA_OBJECT, DATAFLOW_PATH, THIRD_PARTY_SDK, BEHAVIOR, EVIDENCE
    canonical_name: str
    source_module: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorRelationshipDTO(BaseModel):
    source_entity_id: str
    target_entity_id: str
    relationship_type: str = "CALLS"  # REQUIRES, CALLS, READS, WRITES, SENDS, RECEIVES, STORES, LOADS, PARSES, SERIALIZES, DESERIALIZES, ENCRYPTS, DECRYPTS, RESOLVES_TO, REFLECTS_TO, BRIDGES_TO_NATIVE, USES_PERMISSION, TRIGGERS_COMPONENT, CARRIES_DATA, FLOWS_TO, CONNECTS_TO, AUTHENTICATES_WITH, TRUSTS, PINS, CONFIGURES, DEPENDS_ON, CORRELATES_WITH, SUPPORTS, CONTRADICTS
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorChainDTO(BaseModel):
    chain_id: str
    chain_type: str = "MULTI_STAGE_DATA_FLOW"
    nodes: List[str] = Field(default_factory=list)
    edges: List[str] = Field(default_factory=list)
    start_node: str
    end_node: str
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorFindingDTO(BaseModel):
    finding_id: str
    finding_type: str = "SMS_DATA_NETWORK_FLOW"
    category: str = "DATA_TRANSMISSION"  # DATA_COLLECTION, DATA_STORAGE, DATA_TRANSMISSION, THIRD_PARTY_TRANSFER, BACKGROUND_COMMUNICATION, REMOTE_CONFIGURATION, DYNAMIC_CODE_ACCESS, LOCAL_DATA_ENCRYPTION, NETWORK_ENCRYPTION, CERTIFICATE_PINNING, COMPONENT_DATA_TRANSFER, NATIVE_DATA_ACCESS, REFLECTION_DATA_ACCESS, CREDENTIAL_PROCESSING, AUTHENTICATION_FLOW, PAYMENT_DATA_FLOW, LOCATION_DATA_FLOW, CONTACT_DATA_FLOW, SMS_DATA_FLOW, CLIPBOARD_DATA_FLOW, MEDIA_DATA_FLOW, DEVICE_IDENTIFIER_FLOW
    evidence_strength: str = "DIRECT"  # DIRECT, STRONG, MODERATE, WEAK, AMBIGUOUS
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"
    summary: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorConflictDTO(BaseModel):
    conflict_id: str
    conflict_type: str = "CONTRADICTORY_CONFIGURATION"
    evidence_a: str
    evidence_b: str
    resolution_status: str = "CONFLICTED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorSummaryDTO(BaseModel):
    title: str
    summary_text: str
    findings_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorCardDTO(BaseModel):
    card_id: str
    title: str
    category: str
    description: str
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehaviorGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CorrelationGraphDTO(BaseModel):
    source_node: str
    target_node: str
    relationship: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThirdPartyBehaviorDTO(BaseModel):
    sdk_name: str
    sdk_category: str
    data_collected: str
    network_endpoint: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CorrelationMetricsDTO(BaseModel):
    entities_processed: int = 0
    relationships_processed: int = 0
    findings_count: int = 0
    chains_count: int = 0
    conflicts_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BehavioralCorrelationResultDTO(BaseModel):
    entities: List[BehaviorEntityDTO] = Field(default_factory=list)
    relationships: List[BehaviorRelationshipDTO] = Field(default_factory=list)
    chains: List[BehaviorChainDTO] = Field(default_factory=list)
    findings: List[BehaviorFindingDTO] = Field(default_factory=list)
    evidence: List[CorrelationEvidenceDTO] = Field(default_factory=list)
    conflicts: List[BehaviorConflictDTO] = Field(default_factory=list)
    summaries: List[BehaviorSummaryDTO] = Field(default_factory=list)
    cards: List[BehaviorCardDTO] = Field(default_factory=list)
    behavior_graph: BehaviorGraphDTO = Field(default_factory=BehaviorGraphDTO)
    correlation_graph: List[CorrelationGraphDTO] = Field(default_factory=list)
    third_party_behaviors: List[ThirdPartyBehaviorDTO] = Field(default_factory=list)
    metrics: CorrelationMetricsDTO = Field(default_factory=CorrelationMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
