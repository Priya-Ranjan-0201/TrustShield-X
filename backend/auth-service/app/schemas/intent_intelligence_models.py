"""Pydantic v2 DTO Schemas for Intent & Deep Link Intelligence Engine (Phase 3.7 Part 1A.10).

Strictly typed DTOs for intent actions, categories, deep links, navigation graphs,
and intent statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class ActionType(str, Enum):
    SYSTEM = "SYSTEM"
    CUSTOM = "CUSTOM"
    VENDOR = "VENDOR"
    UNKNOWN = "UNKNOWN"


class URIScheme(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    FILE = "FILE"
    CONTENT = "CONTENT"
    PACKAGE = "PACKAGE"
    MARKET = "MARKET"
    TEL = "TEL"
    SMS = "SMS"
    MAILTO = "MAILTO"
    GEO = "GEO"
    CUSTOM = "CUSTOM"


class EnrichedActionDTO(BaseModel):
    action_name: str
    action_type: ActionType = ActionType.CUSTOM
    purpose: Optional[str] = None
    is_system_only: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EnrichedCategoryDTO(BaseModel):
    category_name: str
    is_launcher: bool = False
    is_browsable: bool = False
    is_default: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class EnrichedDeepLinkDTO(BaseModel):
    component_name: str
    scheme: str
    host: Optional[str] = None
    port: Optional[str] = None
    path: Optional[str] = None
    mime_type: Optional[str] = None
    is_app_link: bool = False
    is_browsable: bool = False
    auto_verify: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NavigationNodeDTO(BaseModel):
    source_component: str
    intent_action: str
    target_scheme: Optional[str] = None
    target_host: Optional[str] = None
    destination_component: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class IntentStatisticsDTO(BaseModel):
    total_intent_filters: int = 0
    total_actions: int = 0
    total_categories: int = 0
    total_deep_links: int = 0
    launcher_count: int = 0
    browsable_count: int = 0
    app_links_count: int = 0
    custom_uri_schemes_count: int = 0
    http_links_count: int = 0
    https_links_count: int = 0
    mime_filters_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class IntentIntelligenceResultDTO(BaseModel):
    actions: List[EnrichedActionDTO] = Field(default_factory=list)
    categories: List[EnrichedCategoryDTO] = Field(default_factory=list)
    deep_links: List[EnrichedDeepLinkDTO] = Field(default_factory=list)
    navigation_nodes: List[NavigationNodeDTO] = Field(default_factory=list)
    statistics: IntentStatisticsDTO = Field(default_factory=IntentStatisticsDTO)
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
