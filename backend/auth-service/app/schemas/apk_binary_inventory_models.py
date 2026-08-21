"""Pydantic v2 DTO Schemas for APK Binary Inventory Engine (Phase 3.7 Part 1A.12).

Strictly typed DTOs for binary file entries, file categories, cryptographic fingerprints,
Shannon entropy, and binary inventory statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class FileCategoryEnum(str, Enum):
    DEX = "DEX"
    NATIVE_LIBRARY = "NATIVE_LIBRARY"
    RESOURCE = "RESOURCE"
    ASSET = "ASSET"
    MANIFEST = "MANIFEST"
    CERTIFICATE = "CERTIFICATE"
    META_INF = "META_INF"
    XML = "XML"
    JSON = "JSON"
    IMAGE = "IMAGE"
    FONT = "FONT"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    TEXT = "TEXT"
    SQLITE = "SQLITE"
    DATABASE = "DATABASE"
    ML_MODEL = "ML_MODEL"
    CONFIG = "CONFIG"
    HTML = "HTML"
    JAVASCRIPT = "JAVASCRIPT"
    CSS = "CSS"
    ARCHIVE = "ARCHIVE"
    UNKNOWN_BINARY = "UNKNOWN_BINARY"
    UNKNOWN_RESOURCE = "UNKNOWN_RESOURCE"


class BinaryHashDTO(BaseModel):
    sha256: str
    sha1: str
    md5: str
    crc32: str
    entropy: float = 0.0
    mime_type: str = "application/octet-stream"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BinaryFileEntryDTO(BaseModel):
    file_path: str
    filename: str
    directory: str
    extension: str
    file_category: FileCategoryEnum = FileCategoryEnum.UNKNOWN_BINARY
    uncompressed_size: int = 0
    compressed_size: int = 0
    compression_method: int = 0
    crc32: str = "00000000"
    zip_offset: int = 0
    hashes: BinaryHashDTO

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BinaryStatisticsDTO(BaseModel):
    total_files: int = 0
    total_directories: int = 0
    total_size_bytes: int = 0
    compressed_size_bytes: int = 0
    dex_count: int = 0
    native_library_count: int = 0
    assets_count: int = 0
    resources_count: int = 0
    media_count: int = 0
    config_count: int = 0
    unknown_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class APKBinaryInventoryResultDTO(BaseModel):
    entries: List[BinaryFileEntryDTO] = Field(default_factory=list)
    statistics: BinaryStatisticsDTO = Field(default_factory=BinaryStatisticsDTO)
    inventory_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
