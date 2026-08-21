"""Pydantic v2 DTO Schemas for Enterprise Evidence Normalization, Deduplication, Confidence Fusion & Cross-Engine Finding Consolidation Layer (Phase 3.9 Part 1A.25).

Strictly typed DTOs for canonical entities, canonical evidence, canonical findings, evidence relationships,
evidence independence, evidence groups, finding conflicts, finding lineage, finding versions, finding sources,
finding statistics, confidence fusion, evidence cards, summaries, graphs, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class CanonicalEntityDTO(BaseModel):
    entity_id: str
    entity_type: str = "DOMAIN"  # APK, PACKAGE, CLASS, METHOD, API, PERMISSION, COMPONENT, INTENT, DOMAIN, URL, IP, PORT, CERTIFICATE, HASH, FILE, DATABASE, TABLE, COLUMN, DATA_SOURCE, DATA_SINK, DATAFLOW_PATH, BEHAVIOR, RULE, THREAT_INDICATOR, THREAT_ACTOR, MALWARE_FAMILY, SDK, NATIVE_METHOD, REFLECTION_TARGET
    canonical_value: str
    display_name: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CanonicalEvidenceDTO(BaseModel):
    evidence_id: str
    canonical_entity_id: str
    source_module: str
    evidence_type: str = "NETWORK"  # MANIFEST, PERMISSION, API, DEX, INSTRUCTION, CALL_GRAPH, CONTROL_FLOW, COMPONENT, INTENT, REFLECTION, JNI, CRYPTOGRAPHY, NETWORK, STORAGE, FILESYSTEM, DATAFLOW, BEHAVIOR, THREAT_INTELLIGENCE, YARA, STIX, RULE, CERTIFICATE, HASH, PACKAGE, RESOURCE, NATIVE_LIBRARY, THIRDPARTY_SDK
    evidence_subtype: str = "DOMAIN_OBSERVATION"
    class_name: Optional[str] = None
    method_name: Optional[str] = None
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"
    provenance_reference: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class CanonicalFindingDTO(BaseModel):
    finding_id: str
    finding_type: str = "NETWORK_ENDPOINT_OBSERVED"
    finding_category: str = "NETWORK"
    title: str
    description: str
    status: str = "CORRELATED"  # OBSERVED, CORRELATED, RULE_MATCHED, SUPPORTED, PARTIALLY_SUPPORTED, CONFLICTED, UNRESOLVED, SUPERSEDED, SUPPRESSED, EXPIRED, INVALID
    confidence_level: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW, UNKNOWN
    evidence_strength: str = "STRONG"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW
    resolution_status: str = "RESOLVED"
    source_count: int = 1
    independent_source_count: int = 1
    evidence_count: int = 1
    direct_evidence_count: int = 1
    inferred_evidence_count: int = 0
    contradiction_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceRelationshipDTO(BaseModel):
    source_evidence_id: str
    target_evidence_id: str
    relationship: str = "SUPPORTS"  # SUPPORTS, STRONGLY_SUPPORTS, WEAKLY_SUPPORTS, CONTRADICTS, DERIVED_FROM, DUPLICATES, CORROBORATES, DEPENDS_ON, RESOLVES, PARTIALLY_RESOLVES, SUPERSEDES, EXPIRES

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceIndependenceDTO(BaseModel):
    evidence_id: str
    group_id: str
    independence_type: str = "CROSS_MODULE"
    source_provider: str
    is_independent: bool = True
    reason: str = "Distinct analytical pipeline"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceGroupDTO(BaseModel):
    group_id: str
    group_name: str = "NETWORK_GROUP"
    member_evidence_count: int = 1

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingConflictDTO(BaseModel):
    conflict_id: str
    finding_id: str
    evidence_a_id: str
    evidence_b_id: str
    conflict_type: str = "CONTRADICTORY_CLAIMS"
    explanation: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingLineageDTO(BaseModel):
    lineage_id: str
    finding_id: str
    parent_evidence_id: str
    transformation_step: str = "CORRELATION_TO_CANONICAL"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingVersionDTO(BaseModel):
    finding_id: str
    finding_version: str = "1.0.0"
    engine_version: str = "1.0.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingSourceDTO(BaseModel):
    finding_id: str
    source_module: str
    source_reliability: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingStatisticDTO(BaseModel):
    total_canonical_findings: int = 0
    total_canonical_evidence: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ConfidenceFusionDTO(BaseModel):
    fusion_id: str
    finding_id: str
    fused_confidence: str = "HIGH"
    confidence_ceiling_applied: bool = False
    ceiling_reason: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceCardDTO(BaseModel):
    card_id: str
    title: str
    finding_id: str
    status: str = "CORRELATED"
    confidence: str = "HIGH"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceSummaryDTO(BaseModel):
    title: str
    summary_text: str
    consolidated_findings_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EvidenceGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FindingGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ConsolidationMetricsDTO(BaseModel):
    input_findings_count: int = 0
    canonical_entities_count: int = 0
    canonical_evidence_count: int = 0
    duplicate_evidence_suppressed: int = 0
    merged_findings_count: int = 0
    split_findings_count: int = 0
    conflicted_findings_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ConsolidationResultDTO(BaseModel):
    entities: List[CanonicalEntityDTO] = Field(default_factory=list)
    evidence: List[CanonicalEvidenceDTO] = Field(default_factory=list)
    findings: List[CanonicalFindingDTO] = Field(default_factory=list)
    relationships: List[EvidenceRelationshipDTO] = Field(default_factory=list)
    independence_records: List[EvidenceIndependenceDTO] = Field(default_factory=list)
    groups: List[EvidenceGroupDTO] = Field(default_factory=list)
    conflicts: List[FindingConflictDTO] = Field(default_factory=list)
    lineage_records: List[FindingLineageDTO] = Field(default_factory=list)
    versions: List[FindingVersionDTO] = Field(default_factory=list)
    sources: List[FindingSourceDTO] = Field(default_factory=list)
    statistics: FindingStatisticDTO = Field(default_factory=FindingStatisticDTO)
    confidence_fusions: List[ConfidenceFusionDTO] = Field(default_factory=list)
    cards: List[EvidenceCardDTO] = Field(default_factory=list)
    summaries: List[EvidenceSummaryDTO] = Field(default_factory=list)
    evidence_graph: EvidenceGraphDTO = Field(default_factory=EvidenceGraphDTO)
    finding_graph: FindingGraphDTO = Field(default_factory=FindingGraphDTO)
    metrics: ConsolidationMetricsDTO = Field(default_factory=ConsolidationMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
