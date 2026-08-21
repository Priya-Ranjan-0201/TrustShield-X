"""Pydantic v2 DTO Schemas for Enterprise Dataflow & Information-Flow Intelligence Engine (Phase 3.9 Part 1A.21).

Strictly typed DTOs for nodes, edges, paths, sources, sinks, taint labels, transformations,
evidence, confidence, information-flow graphs, source-sink graphs, flow boundaries,
third-party flows, JNI flows, reflection flows, intent flows, metrics, and result DTO.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class DataflowNodeDTO(BaseModel):
    node_id: str
    node_type: str = "SOURCE"  # SOURCE, VARIABLE, PARAMETER, RETURN_VALUE, FIELD, ARRAY_ELEMENT, CONSTANT, OBJECT, METHOD, API, PARSER, TRANSFORMER, ENCRYPTION, DECRYPTION, SERIALIZER, DESERIALIZER, STORAGE, DATABASE, FILE, PREFERENCE, CACHE, URI, INTENT, BUNDLE, CONTENT_PROVIDER, NETWORK_ENDPOINT, NATIVE_FUNCTION, REFLECTION, SINK, UNKNOWN
    label: str
    class_name: str
    method_name: str
    instruction_offset: int = 0
    data_category: str = "IDENTITY"
    confidence: str = "HIGH"  # VERY_HIGH, HIGH, MEDIUM, LOW, VERY_LOW
    resolution_status: str = "RESOLVED"  # RESOLVED, PARTIALLY_RESOLVED, UNRESOLVED, INFERRED

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowEdgeDTO(BaseModel):
    source_node_id: str
    target_node_id: str
    edge_type: str = "ASSIGN"  # ASSIGN, COPY, MOVE, CAST, CONCATENATE, FORMAT, PARSE, SERIALIZE, DESERIALIZE, ENCODE, DECODE, ENCRYPT, DECRYPT, COMPRESS, DECOMPRESS, ARGUMENT, RETURN, FIELD_WRITE, FIELD_READ, ARRAY_WRITE, ARRAY_READ, INTENT_PUT, INTENT_GET, BUNDLE_PUT, BUNDLE_GET, URI_BUILD, URI_PARSE, FILE_WRITE, FILE_READ, DATABASE_INSERT, DATABASE_QUERY, DATABASE_UPDATE, DATABASE_DELETE, NETWORK_SEND, NETWORK_RECEIVE, REFLECTION_CALL, JNI_CALL, CALLBACK, THROW, CATCH
    caller_method: str
    instruction_offset: int = 0
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowSourceDTO(BaseModel):
    source_id: str
    source_type: str = "LOCATION_API"
    data_category: str = "LOCATION"
    api_canonical_id: str
    source_class: str
    source_method: str
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowSinkDTO(BaseModel):
    sink_id: str
    sink_type: str = "NETWORK_HTTP"
    target_identifier: str
    sink_class: str
    sink_method: str
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowPathDTO(BaseModel):
    path_id: str
    source_id: str
    sink_id: str
    path_nodes: List[str] = Field(default_factory=list)
    flow_classification: str = "SOURCE_TO_NETWORK"  # LOCAL_ONLY, LOCAL_STORAGE, LOCAL_TO_NETWORK, NETWORK_TO_LOCAL, SOURCE_TO_STORAGE, SOURCE_TO_NETWORK, SOURCE_TO_THIRDPARTY, INTER_COMPONENT, INTER_PROCESS, NATIVE_BOUNDARY, CRYPTOGRAPHIC_BOUNDARY, SERIALIZATION_BOUNDARY, UNKNOWN_FLOW
    confidence: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowTaintLabelDTO(BaseModel):
    node_id: str
    taint_label: str = "TAINT_LOCATION"  # TAINT_LOCATION, TAINT_CONTACT, TAINT_SMS, TAINT_TOKEN, TAINT_CREDENTIAL, TAINT_PAYMENT, TAINT_HEALTH, TAINT_DEVICE_ID, TAINT_CLIPBOARD, TAINT_PERSONAL_DATA
    original_taint: str = "LOCATION"
    is_sanitized: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowTransformationDTO(BaseModel):
    caller_method: str
    transformation_type: str = "SERIALIZATION"  # SERIALIZATION, ENCRYPTION, COMPRESSION, CONCATENATION, PARSING
    input_node_id: str
    output_node_id: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FlowBoundaryDTO(BaseModel):
    boundary_type: str = "CRYPTOGRAPHIC_BOUNDARY"  # CRYPTOGRAPHIC_BOUNDARY, SERIALIZATION_BOUNDARY, REFLECTION_BOUNDARY, JNI_BOUNDARY, THIRD_PARTY_SDK
    source_method: str
    target_method: str
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ThirdPartyDataflowDTO(BaseModel):
    source_id: str
    sdk_name: str = "Google Analytics"
    sdk_category: str = "ANALYTICS"  # ANALYTICS, ADVERTISING, CRASH_REPORTING, AUTHENTICATION, PAYMENT
    target_endpoint: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class JNIDataflowDTO(BaseModel):
    java_method: str
    native_symbol: str
    library_name: str
    direction: str = "JAVA_TO_NATIVE"  # JAVA_TO_NATIVE, NATIVE_TO_JAVA

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReflectionDataflowDTO(BaseModel):
    caller_method: str
    reflection_target: str
    resolution_status: str = "RESOLVED"  # RESOLVED, PARTIALLY_RESOLVED, UNRESOLVED

    model_config = ConfigDict(frozen=True, from_attributes=True)


class IntentDataflowDTO(BaseModel):
    source_component: str
    target_component: str
    extra_key: str
    extra_type: str = "STRING"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowEvidenceDTO(BaseModel):
    dex_id: str
    class_name: str
    method_name: str
    instruction_offset: int = 0
    evidence_type: str = "SOURCE_TO_SINK_EDGE"
    raw_evidence: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowConfidenceDTO(BaseModel):
    path_id: str
    confidence_score: float = 0.95
    confidence_level: str = "HIGH"
    resolution_status: str = "RESOLVED"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class InformationFlowGraphDTO(BaseModel):
    nodes_count: int = 0
    edges_count: int = 0
    sources_count: int = 0
    sinks_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SourceSinkGraphDTO(BaseModel):
    source_node: str
    sink_node: str
    path_length: int = 2

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowMetricsDTO(BaseModel):
    methods_analyzed: int = 0
    instructions_analyzed: int = 0
    sources_count: int = 0
    sinks_count: int = 0
    paths_count: int = 0
    taint_labels_count: int = 0
    unresolved_boundaries_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DataflowResultDTO(BaseModel):
    nodes: List[DataflowNodeDTO] = Field(default_factory=list)
    edges: List[DataflowEdgeDTO] = Field(default_factory=list)
    paths: List[DataflowPathDTO] = Field(default_factory=list)
    sources: List[DataflowSourceDTO] = Field(default_factory=list)
    sinks: List[DataflowSinkDTO] = Field(default_factory=list)
    taint_labels: List[DataflowTaintLabelDTO] = Field(default_factory=list)
    transformations: List[DataflowTransformationDTO] = Field(default_factory=list)
    boundaries: List[FlowBoundaryDTO] = Field(default_factory=list)
    third_party_flows: List[ThirdPartyDataflowDTO] = Field(default_factory=list)
    jni_flows: List[JNIDataflowDTO] = Field(default_factory=list)
    reflection_flows: List[ReflectionDataflowDTO] = Field(default_factory=list)
    intent_flows: List[IntentDataflowDTO] = Field(default_factory=list)
    evidence: List[DataflowEvidenceDTO] = Field(default_factory=list)
    confidence: List[DataflowConfidenceDTO] = Field(default_factory=list)
    info_graph: InformationFlowGraphDTO = Field(default_factory=InformationFlowGraphDTO)
    source_sink_graph: List[SourceSinkGraphDTO] = Field(default_factory=list)
    metrics: DataflowMetricsDTO = Field(default_factory=DataflowMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    graphml_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    analysis_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
