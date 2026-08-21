"""Pydantic v2 DTO Schemas for Enterprise Reflection & Dynamic Code Loading Intelligence Engine (Phase 3.7 Part 1A.17).

Strictly typed DTOs for reflection calls, target resolution, dynamic class loaders,
native library loading, JNI bindings, hidden APIs, reflection graph, and metrics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ReflectionCallDTO(BaseModel):
    caller_method: str
    reflection_api: str  # Class.forName, Method.invoke, Field.get, etc.
    target_class: Optional[str] = None
    target_member: Optional[str] = None
    offset: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReflectionTargetDTO(BaseModel):
    canonical_target: str
    target_type: str = "CLASS"  # CLASS, METHOD, FIELD, CONSTRUCTOR
    is_resolved: bool = True

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DynamicClassDTO(BaseModel):
    caller_method: str
    loader_type: str  # DexClassLoader, InMemoryDexClassLoader, etc.
    dex_path: Optional[str] = None
    is_memory_only: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NativeLoadingDTO(BaseModel):
    caller_method: str
    library_name: str
    load_api: str = "System.loadLibrary"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class JNIBindingDTO(BaseModel):
    native_method: str
    java_class: str
    symbol_name: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class HiddenAPIDTO(BaseModel):
    api_signature: str
    access_mechanism: str = "REFLECTION"
    restriction_level: str = "GREYLIST"  # GREYLIST, BLACKLIST, LIGHT_GREYLIST, DARK_GREYLIST

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReflectionGraphEdgeDTO(BaseModel):
    caller_method: str
    target_symbol: str
    invocation_type: str = "REFLECTIVE_INVOKE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DynamicInvocationDTO(BaseModel):
    source_symbol: str
    resolved_target: str
    confidence: float = 1.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReflectionMetricsDTO(BaseModel):
    reflection_calls_count: int = 0
    dynamic_loaders_count: int = 0
    native_loads_count: int = 0
    hidden_apis_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReflectionResultDTO(BaseModel):
    reflection_calls: List[ReflectionCallDTO] = Field(default_factory=list)
    targets: List[ReflectionTargetDTO] = Field(default_factory=list)
    dynamic_classes: List[DynamicClassDTO] = Field(default_factory=list)
    native_loads: List[NativeLoadingDTO] = Field(default_factory=list)
    jni_bindings: List[JNIBindingDTO] = Field(default_factory=list)
    hidden_apis: List[HiddenAPIDTO] = Field(default_factory=list)
    reflection_graph: List[ReflectionGraphEdgeDTO] = Field(default_factory=list)
    dynamic_invocations: List[DynamicInvocationDTO] = Field(default_factory=list)
    metrics: ReflectionMetricsDTO = Field(default_factory=ReflectionMetricsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
