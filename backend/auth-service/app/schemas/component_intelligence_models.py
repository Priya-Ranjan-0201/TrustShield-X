"""Pydantic v2 DTO Schemas for Android Component Intelligence Engine (Phase 3.7 Part 1A.9).

Strictly typed DTOs for enriched components, intent filters, launch intelligence,
export statuses, process metadata, relationships, and component statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ExportStatus(str, Enum):
    EXPLICIT_EXPORTED = "EXPLICIT_EXPORTED"
    IMPLICIT_EXPORTED = "IMPLICIT_EXPORTED"
    DEFAULT_EXPORTED = "DEFAULT_EXPORTED"
    NON_EXPORTED = "NON_EXPORTED"
    UNKNOWN = "UNKNOWN"


class ProcessType(str, Enum):
    DEFAULT = "DEFAULT"
    CUSTOM = "CUSTOM"
    SHARED = "SHARED"
    ISOLATED = "ISOLATED"
    REMOTE = "REMOTE"
    PERSISTENT = "PERSISTENT"


class EnrichedIntentFilterDTO(BaseModel):
    actions: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    schemes: List[str] = Field(default_factory=list)
    hosts: List[str] = Field(default_factory=list)
    ports: List[str] = Field(default_factory=list)
    paths: List[str] = Field(default_factory=list)
    mime_types: List[str] = Field(default_factory=list)
    priority: int = 0
    auto_verify: bool = False
    is_deep_link: bool = False
    is_launcher: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EnrichedComponentDTO(BaseModel):
    name: str
    component_type: str
    exported_status: ExportStatus = ExportStatus.NON_EXPORTED
    is_enabled: bool = True
    permission: Optional[str] = None
    process_name: str = "default"
    process_type: ProcessType = ProcessType.DEFAULT
    is_launcher: bool = False
    is_foreground: bool = False
    is_isolated: bool = False
    authorities: Optional[str] = None
    launch_mode: Optional[str] = None
    task_affinity: Optional[str] = None
    theme: Optional[str] = None
    intent_filters: List[EnrichedIntentFilterDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ComponentRelationshipDTO(BaseModel):
    parent_component: str
    child_component: str
    relationship_type: str  # alias, intent_target, provider_authority

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ProcessIntelligenceDTO(BaseModel):
    process_name: str
    process_type: ProcessType
    component_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ComponentStatisticsDTO(BaseModel):
    total_components: int = 0
    activities_count: int = 0
    services_count: int = 0
    receivers_count: int = 0
    providers_count: int = 0
    intent_filters_count: int = 0
    launcher_activities_count: int = 0
    foreground_services_count: int = 0
    exported_count: int = 0
    non_exported_count: int = 0
    deep_link_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ComponentIntelligenceResultDTO(BaseModel):
    components: List[EnrichedComponentDTO] = Field(default_factory=list)
    relationships: List[ComponentRelationshipDTO] = Field(default_factory=list)
    processes: List[ProcessIntelligenceDTO] = Field(default_factory=list)
    statistics: ComponentStatisticsDTO = Field(default_factory=ComponentStatisticsDTO)
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
