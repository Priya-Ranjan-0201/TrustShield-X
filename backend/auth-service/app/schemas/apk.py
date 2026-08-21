"""Pydantic v2 REST API Response DTO Contracts for AI Android APK Security Engine (Phase 3.7 Part 1A Message 3C.1).

All DTOs are strictly typed and wrapped in ResponseEnvelope[T].
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class APKUploadRequest(BaseModel):
    filename: Optional[str] = None
    mime_type: Optional[str] = "application/vnd.android.package-archive"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKCertificateDTO(BaseModel):
    subject: Optional[str] = None
    issuer: Optional[str] = None
    serial_number: Optional[str] = None
    signature_algorithm: Optional[str] = None
    public_key_algorithm: Optional[str] = None
    public_key_size: Optional[int] = None
    sha256: str = ""
    sha1: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None
    expired: bool = False
    self_signed: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKPermissionDTO(BaseModel):
    permission_name: str
    protection_level: Optional[str] = None
    declared_by_app: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKDEXDTO(BaseModel):
    filename: str
    sha256: str
    size: int
    method_count: int = 0
    class_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKLibraryDTO(BaseModel):
    library_name: str
    architecture: str
    sha256: str
    size: int

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKResourceDTO(BaseModel):
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

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKManifestDTO(BaseModel):
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    min_sdk: Optional[int] = None
    target_sdk: Optional[int] = None
    compile_sdk: Optional[int] = None
    permissions_count: int = 0
    activities_count: int = 0
    services_count: int = 0
    receivers_count: int = 0
    providers_count: int = 0
    deep_links: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKResponse(BaseModel):
    scan_id: str
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    application_label: Optional[str] = None
    min_sdk: Optional[int] = None
    target_sdk: Optional[int] = None
    compile_sdk: Optional[int] = None
    apk_size: int = 0
    apk_sha256: str = ""
    parsed_successfully: bool = True
    manifest: Optional[APKManifestDTO] = None
    permissions: List[APKPermissionDTO] = Field(default_factory=list)
    dex_files: List[APKDEXDTO] = Field(default_factory=list)
    native_libraries: List[APKLibraryDTO] = Field(default_factory=list)
    certificates: List[APKCertificateDTO] = Field(default_factory=list)
    resources: Optional[APKResourceDTO] = None
    processing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKSummary(BaseModel):
    scan_id: str
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    application_label: Optional[str] = None
    apk_size: int = 0
    apk_sha256: str = ""
    permissions_count: int = 0
    dex_count: int = 0
    native_lib_count: int = 0
    parsed_successfully: bool = True
    created_at: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKHistoryItem(BaseModel):
    scan_id: str
    package_name: Optional[str] = None
    version_name: Optional[str] = None
    apk_size: int = 0
    apk_sha256: str = ""
    certificate_sha256: Optional[str] = None
    parsed_successfully: bool = True
    created_at: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKHistoryResponse(BaseModel):
    total_count: int
    limit: int
    offset: int
    items: List[APKHistoryItem]

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKDeleteResponse(BaseModel):
    scan_id: str
    deleted: bool
    message: str

    model_config = ConfigDict(frozen=True, from_attributes=True)
