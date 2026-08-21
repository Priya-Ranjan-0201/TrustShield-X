"""Pydantic v2 DTO Models for AI Android APK Security Engine (Phase 3.7 Part 1A Message 2).

All models are strongly typed, immutable/frozen, and strictly validated.
No generic dicts or untyped JSON.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class PermissionInfo(BaseModel):
    name: str
    protection_level: Optional[str] = None
    declared_by_app: bool = False
    is_system_permission: bool = True

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ActivityInfo(BaseModel):
    name: str
    exported: Optional[bool] = None
    enabled: bool = True
    permission: Optional[str] = None
    launch_mode: Optional[str] = None
    task_affinity: Optional[str] = None
    screen_orientation: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ServiceInfo(BaseModel):
    name: str
    exported: Optional[bool] = None
    enabled: bool = True
    foreground: bool = False
    permission: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReceiverInfo(BaseModel):
    name: str
    exported: Optional[bool] = None
    enabled: bool = True
    permission: Optional[str] = None
    intent_filters: List[Dict[str, Any]] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ProviderInfo(BaseModel):
    name: str
    authority: Optional[str] = None
    exported: Optional[bool] = None
    permission: Optional[str] = None
    grant_uri_permissions: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ManifestMetadata(BaseModel):
    permissions: List[PermissionInfo] = Field(default_factory=list)
    activities: List[ActivityInfo] = Field(default_factory=list)
    services: List[ServiceInfo] = Field(default_factory=list)
    receivers: List[ReceiverInfo] = Field(default_factory=list)
    providers: List[ProviderInfo] = Field(default_factory=list)
    intent_filters: List[Dict[str, Any]] = Field(default_factory=list)
    deep_links: List[str] = Field(default_factory=list)
    queries: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    meta_data: Dict[str, str] = Field(default_factory=dict)
    application_flags: Dict[str, bool] = Field(default_factory=dict)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXMetadata(BaseModel):
    filename: str
    size: int
    sha256: str
    class_count: int = 0
    method_count: int = 0
    package_count: int = 0
    index: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXSummary(BaseModel):
    total_dex_files: int = 0
    largest_dex_name: Optional[str] = None
    largest_dex_bytes: int = 0
    smallest_dex_bytes: int = 0
    combined_size_bytes: int = 0
    average_size_bytes: float = 0.0
    dex_files: List[DEXMetadata] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NativeLibraryMetadata(BaseModel):
    library_name: str
    architecture: str  # armeabi, armeabi-v7a, arm64-v8a, x86, x86_64, riscv64
    size: int
    sha256: str
    path: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class NativeLibrarySummary(BaseModel):
    library_count: int = 0
    architectures_present: List[str] = Field(default_factory=list)
    largest_library_name: Optional[str] = None
    largest_library_bytes: int = 0
    average_library_size_bytes: float = 0.0
    libraries: List[NativeLibraryMetadata] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ResourceInventory(BaseModel):
    resource_count: int = 0
    asset_count: int = 0
    xml_count: int = 0
    image_count: int = 0
    font_count: int = 0
    audio_count: int = 0
    video_count: int = 0
    binary_count: int = 0
    largest_resource_name: Optional[str] = None
    largest_resource_bytes: int = 0
    average_resource_size_bytes: float = 0.0
    total_compressed_bytes: int = 0
    total_uncompressed_bytes: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKMetadata(BaseModel):
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    application_label: Optional[str] = None
    application_class: Optional[str] = None
    compile_sdk: Optional[int] = None
    min_sdk: Optional[int] = None
    target_sdk: Optional[int] = None
    shared_user_id: Optional[str] = None
    install_location: Optional[str] = None
    debuggable: bool = False
    allow_backup: bool = True
    allow_cleartext: bool = False
    network_security_config: Optional[str] = None
    icon_path: Optional[str] = None
    package_size: int = 0
    apk_sha256: str = ""
    dex_count: int = 0
    native_library_count: int = 0
    asset_count: int = 0
    resource_count: int = 0
    certificate_count: int = 0
    manifest_metadata: Optional[ManifestMetadata] = None
    dex_summary: Optional[DEXSummary] = None
    native_library_summary: Optional[NativeLibrarySummary] = None
    resource_inventory: Optional[ResourceInventory] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)
