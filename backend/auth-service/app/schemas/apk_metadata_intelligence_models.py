"""Pydantic v2 DTO Schemas for APK Metadata & Package Intelligence Engine (Phase 3.7 Part 1A.11).

Strictly typed DTOs for package identity, semantic versioning, SDK profiles,
installation parameters, application flags, and resource references.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class InstallLocation(str, Enum):
    INTERNAL = "INTERNAL"
    AUTO = "AUTO"
    EXTERNAL = "EXTERNAL"
    INSTANT = "INSTANT"


class VersionIntelligenceDTO(BaseModel):
    version_name: str = "1.0"
    version_code: int = 1
    major: int = 1
    minor: int = 0
    patch: int = 0
    build: Optional[int] = None
    version_format: str = "SEMANTIC"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class SDKProfileDTO(BaseModel):
    min_sdk: int = 21
    target_sdk: int = 33
    compile_sdk: Optional[int] = 33
    max_sdk: Optional[int] = None
    platform_version: str = "Android 13.0"
    generation_name: str = "Android 13 (Tiramisu)"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ApplicationFlagsDTO(BaseModel):
    is_debuggable: bool = False
    is_persistent: bool = False
    is_test_only: bool = False
    allow_backup: bool = True
    large_heap: bool = False
    uses_cleartext: bool = False
    supports_rtl: bool = True
    direct_boot_aware: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ResourceReferencesDTO(BaseModel):
    app_label: Optional[str] = None
    app_class: Optional[str] = None
    icon_ref: Optional[str] = None
    round_icon_ref: Optional[str] = None
    banner_ref: Optional[str] = None
    logo_ref: Optional[str] = None
    theme_ref: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKMetadataIntelligenceResultDTO(BaseModel):
    package_name: str = "com.unknown.app"
    version_info: VersionIntelligenceDTO = Field(default_factory=VersionIntelligenceDTO)
    sdk_profile: SDKProfileDTO = Field(default_factory=SDKProfileDTO)
    install_location: InstallLocation = InstallLocation.AUTO
    app_flags: ApplicationFlagsDTO = Field(default_factory=ApplicationFlagsDTO)
    resources: ResourceReferencesDTO = Field(default_factory=ResourceReferencesDTO)
    metadata_fields_count: int = 0
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
