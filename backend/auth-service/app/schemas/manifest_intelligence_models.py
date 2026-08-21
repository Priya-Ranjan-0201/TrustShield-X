"""Pydantic v2 DTO Schemas for AndroidManifest Intelligence Engine (Phase 3.7 Part 1A.5).

Strictly typed DTOs for package attributes, SDK levels, Activities, Services, Receivers, Providers,
Intent Filters, Features, Libraries, and Permission references.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class SDKCategory(str, Enum):
    DEPRECATED = "DEPRECATED"  # API < 21
    LEGACY = "LEGACY"          # 21 <= API < 23
    MODERN = "MODERN"          # 23 <= API <= 34
    FUTURE = "FUTURE"          # API > 34
    UNKNOWN = "UNKNOWN"


class ComponentType(str, Enum):
    ACTIVITY = "ACTIVITY"
    SERVICE = "SERVICE"
    RECEIVER = "RECEIVER"
    PROVIDER = "PROVIDER"


class IntentFilterDTO(BaseModel):
    actions: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    schemes: List[str] = Field(default_factory=list)
    hosts: List[str] = Field(default_factory=list)
    ports: List[str] = Field(default_factory=list)
    mime_types: List[str] = Field(default_factory=list)
    path_prefixes: List[str] = Field(default_factory=list)
    path_patterns: List[str] = Field(default_factory=list)
    priority: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ComponentDTO(BaseModel):
    name: str
    component_type: ComponentType
    exported: Optional[bool] = None
    enabled: bool = True
    permission: Optional[str] = None
    process: Optional[str] = None
    launch_mode: Optional[str] = None
    screen_orientation: Optional[str] = None
    task_affinity: Optional[str] = None
    theme: Optional[str] = None
    config_changes: Optional[str] = None
    foreground_service_type: Optional[str] = None
    authorities: Optional[str] = None
    grant_uri_permissions: bool = False
    read_permission: Optional[str] = None
    write_permission: Optional[str] = None
    multiprocess: bool = False
    syncable: bool = False
    priority: int = 0
    intent_filters: List[IntentFilterDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FeatureDTO(BaseModel):
    name: str
    required: bool = True
    gl_version: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class LibraryDTO(BaseModel):
    name: str
    required: bool = True

    model_config = ConfigDict(frozen=True, from_attributes=True)


class PermissionRefDTO(BaseModel):
    name: str
    protection_level: Optional[str] = None
    declared: bool = False
    requested: bool = True
    is_custom: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class QueryDTO(BaseModel):
    query_type: str  # package, intent, provider
    target: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ManifestIntelligenceDTO(BaseModel):
    # Package Attributes
    package_name: str
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    min_sdk: Optional[int] = None
    target_sdk: Optional[int] = None
    compile_sdk: Optional[int] = None
    sdk_category: SDKCategory = SDKCategory.UNKNOWN
    install_location: Optional[str] = None
    shared_user_id: Optional[str] = None
    debuggable: bool = False
    test_only: bool = False
    allow_backup: bool = True
    backup_agent: Optional[str] = None
    network_security_config: Optional[str] = None
    uses_cleartext_traffic: bool = False
    supports_rtl: bool = False
    hardware_accelerated: bool = True
    extract_native_libs: bool = True
    profileable: bool = False
    isolated_process: bool = False
    gwp_asan_mode: Optional[str] = None

    # Application Attributes
    application_label: Optional[str] = None
    application_icon: Optional[str] = None
    theme: Optional[str] = None
    banner: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    application_permission: Optional[str] = None
    process_name: Optional[str] = None
    task_affinity: Optional[str] = None
    vm_safe_mode: bool = False
    large_heap: bool = False
    persistent: bool = False
    has_code: bool = True
    allow_task_reparenting: bool = False
    resizeable_activity: Optional[bool] = None
    uses_non_sdk_api: bool = False

    # Component Collections
    activities: List[ComponentDTO] = Field(default_factory=list)
    services: List[ComponentDTO] = Field(default_factory=list)
    receivers: List[ComponentDTO] = Field(default_factory=list)
    providers: List[ComponentDTO] = Field(default_factory=list)

    # Features, Libraries, Queries & Permissions
    features: List[FeatureDTO] = Field(default_factory=list)
    libraries: List[LibraryDTO] = Field(default_factory=list)
    permissions: List[PermissionRefDTO] = Field(default_factory=list)
    queries: List[QueryDTO] = Field(default_factory=list)

    # Telemetry Metrics
    parsing_time_ms: int = 0
    xml_size_bytes: int = 0
    total_components_count: int = 0

    @property
    def application_flags(self) -> Dict[str, Any]:
        return {
            "debuggable": self.debuggable,
            "allow_backup": self.allow_backup,
            "uses_cleartext_traffic": self.uses_cleartext_traffic,
            "supports_rtl": self.supports_rtl,
            "hardware_accelerated": self.hardware_accelerated,
        }

    model_config = ConfigDict(frozen=True, from_attributes=True)
