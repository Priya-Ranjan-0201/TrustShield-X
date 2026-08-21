"""Pydantic v2 DTO Schemas for Enterprise Sensitive Android API Intelligence Engine (Phase 3.7 Part 1A.16).

Strictly typed DTOs for API catalog entries, semantic capabilities, API usage,
framework fingerprinting, library inventorying, cross-references, and statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class APICapabilityEnum(str, Enum):
    NETWORK = "NETWORK"
    CRYPTO = "CRYPTO"
    FILESYSTEM = "FILESYSTEM"
    LOCATION = "LOCATION"
    CAMERA = "CAMERA"
    MICROPHONE = "MICROPHONE"
    SMS = "SMS"
    TELEPHONY = "TELEPHONY"
    REFLECTION = "REFLECTION"
    DYNAMIC_LOADING = "DYNAMIC_LOADING"
    IPC = "IPC"
    WEBVIEW = "WEBVIEW"
    BIOMETRICS = "BIOMETRICS"
    MACHINE_LEARNING = "MACHINE_LEARNING"
    DEVICE_INFO = "DEVICE_INFO"
    SYSTEM = "SYSTEM"
    OTHERS = "OTHERS"


class APICatalogEntryDTO(BaseModel):
    canonical_id: str
    package_name: str
    class_name: str
    method_name: str
    signature: str
    framework: str = "ANDROID_SDK"
    min_sdk: int = 1
    deprecated: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APICapabilityEntryDTO(BaseModel):
    api_canonical_id: str
    capability: APICapabilityEnum = APICapabilityEnum.OTHERS

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APIUsageDTO(BaseModel):
    caller_method: str
    api_canonical_id: str
    offset: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APIFrameworkDTO(BaseModel):
    framework_name: str
    version: Optional[str] = "1.0"
    detected_by: str = "PACKAGE_PREFIX"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class LibraryInventoryDTO(BaseModel):
    library_name: str
    version: Optional[str] = "1.0"
    package_prefix: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APICrossRefDTO(BaseModel):
    source_symbol: str
    api_canonical_id: str
    xref_type: str = "INVOKE"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APIStatisticsDTO(BaseModel):
    total_apis: int = 0
    unique_frameworks: int = 0
    most_used_capability: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APIIntelligenceResultDTO(BaseModel):
    api_catalog: List[APICatalogEntryDTO] = Field(default_factory=list)
    capabilities: List[APICapabilityEntryDTO] = Field(default_factory=list)
    api_usage: List[APIUsageDTO] = Field(default_factory=list)
    frameworks: List[APIFrameworkDTO] = Field(default_factory=list)
    libraries: List[LibraryInventoryDTO] = Field(default_factory=list)
    xrefs: List[APICrossRefDTO] = Field(default_factory=list)
    statistics: APIStatisticsDTO = Field(default_factory=APIStatisticsDTO)
    json_export: Optional[str] = None
    csv_export: Optional[str] = None
    dot_export: Optional[str] = None
    mermaid_export: Optional[str] = None
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
