"""Pydantic v2 DTO Schemas for DEX & Multi-DEX Intelligence Engine (Phase 3.7 Part 1A.6).

Strictly typed DTOs for DEX headers, sections, Classes, Methods, Fields, Packages,
String Pool statistics, and Multi-DEX aggregates.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class DEXHeaderDTO(BaseModel):
    magic_version: str
    checksum: str
    checksum_valid: bool = True
    sha1_signature: str
    file_size: int
    header_size: int = 112
    endian_tag: str
    link_size: int = 0
    link_off: int = 0
    map_off: int = 0
    string_ids_size: int = 0
    string_ids_off: int = 0
    type_ids_size: int = 0
    type_ids_off: int = 0
    proto_ids_size: int = 0
    proto_ids_off: int = 0
    field_ids_size: int = 0
    field_ids_off: int = 0
    method_ids_size: int = 0
    method_ids_off: int = 0
    class_defs_size: int = 0
    class_defs_off: int = 0
    data_size: int = 0
    data_off: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FieldDTO(BaseModel):
    name: str
    field_type: str
    access_flags: int = 0
    is_static: bool = False
    is_final: bool = False
    is_volatile: bool = False
    is_transient: bool = False
    is_synthetic: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class MethodDTO(BaseModel):
    name: str
    return_type: str
    parameter_types: List[str] = Field(default_factory=list)
    access_flags: int = 0
    is_direct: bool = False
    is_virtual: bool = False
    is_native: bool = False
    is_abstract: bool = False
    is_constructor: bool = False
    is_static: bool = False
    is_synthetic: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ClassDTO(BaseModel):
    name: str
    package_name: str
    superclass: Optional[str] = None
    interfaces: List[str] = Field(default_factory=list)
    access_flags: int = 0
    is_interface: bool = False
    is_enum: bool = False
    is_annotation: bool = False
    is_abstract: bool = False
    is_concrete: bool = True
    source_file: Optional[str] = None
    methods: List[MethodDTO] = Field(default_factory=list)
    fields: List[FieldDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class PackageDTO(BaseModel):
    package_name: str
    class_count: int = 0
    depth: int = 1

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXFileIntelligenceDTO(BaseModel):
    dex_name: str
    dex_order: int = 0
    sha256: str
    sha1: str
    file_size: int
    header: DEXHeaderDTO
    classes: List[ClassDTO] = Field(default_factory=list)
    total_strings_count: int = 0
    unique_strings_count: int = 0
    avg_string_length: float = 0.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class MultiDEXIntelligenceDTO(BaseModel):
    total_dex_files: int = 0
    total_classes_count: int = 0
    total_methods_count: int = 0
    total_fields_count: int = 0
    total_packages_count: int = 0
    native_methods_count: int = 0
    dex_files: List[DEXFileIntelligenceDTO] = Field(default_factory=list)
    packages: List[PackageDTO] = Field(default_factory=list)
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
