"""Pydantic v2 DTO Schemas for DEX Structure Intelligence Engine (Phase 3.7 Part 1A.13).

Strictly typed DTOs for DEX headers, package trees, classes, methods, fields,
strings, types, reference graphs, and structural statistics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class DEXHeaderDTO(BaseModel):
    dex_version: str = "035"
    magic: str = "dex\n035\x00"
    checksum: int = 0
    sha1: str = ""
    file_size: int = 0
    header_size: int = 112
    endian_tag: int = 0x12345678
    link_size: int = 0
    link_offset: int = 0
    map_offset: int = 0
    string_count: int = 0
    type_count: int = 0
    proto_count: int = 0
    field_count: int = 0
    method_count: int = 0
    class_count: int = 0
    data_size: int = 0
    data_offset: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class PackageNodeDTO(BaseModel):
    package_name: str
    parent_package: Optional[str] = None
    depth: int = 0
    class_count: int = 0
    method_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ClassStructureDTO(BaseModel):
    full_name: str
    simple_name: str
    package_name: str
    superclass: Optional[str] = "java.lang.Object"
    interfaces: List[str] = Field(default_factory=list)
    access_flags: int = 1
    is_abstract: bool = False
    is_final: bool = False
    is_public: bool = True
    is_private: bool = False
    is_protected: bool = False
    is_static: bool = False
    is_synthetic: bool = False
    is_inner: bool = False
    is_anonymous: bool = False
    outer_class: Optional[str] = None
    generic_signature: Optional[str] = None
    source_file: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class MethodStructureDTO(BaseModel):
    method_name: str
    class_name: str
    package_name: str
    return_type: str = "V"
    parameter_types: List[str] = Field(default_factory=list)
    access_flags: int = 1
    is_constructor: bool = False
    is_static: bool = False
    is_abstract: bool = False
    is_native: bool = False
    is_synchronized: bool = False
    is_bridge: bool = False
    is_synthetic: bool = False
    method_idx: int = 0
    code_offset: int = 0
    register_count: int = 0
    instruction_count: int = 0
    try_catch_count: int = 0
    annotation_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class FieldStructureDTO(BaseModel):
    field_name: str
    class_name: str
    package_name: str
    field_type: str = "Ljava/lang/Object;"
    access_flags: int = 1
    is_static: bool = False
    is_final: bool = False
    is_constant: bool = False
    is_enum: bool = False
    field_idx: int = 0
    signature: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class StringEntryDTO(BaseModel):
    string_value: str
    length: int = 0
    string_hash: str = ""
    offset: int = 0
    referenced_count: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class TypeEntryDTO(BaseModel):
    type_name: str
    kind: str = "OBJECT"  # PRIMITIVE, OBJECT, ARRAY, INTERFACE

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXStructureStatisticsDTO(BaseModel):
    total_packages: int = 0
    total_classes: int = 0
    total_methods: int = 0
    total_fields: int = 0
    total_strings: int = 0
    avg_methods_per_class: float = 0.0
    largest_package: Optional[str] = None
    largest_class: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXStructureResultDTO(BaseModel):
    headers: List[DEXHeaderDTO] = Field(default_factory=list)
    packages: List[PackageNodeDTO] = Field(default_factory=list)
    classes: List[ClassStructureDTO] = Field(default_factory=list)
    methods: List[MethodStructureDTO] = Field(default_factory=list)
    fields: List[FieldStructureDTO] = Field(default_factory=list)
    strings: List[StringEntryDTO] = Field(default_factory=list)
    types: List[TypeEntryDTO] = Field(default_factory=list)
    statistics: DEXStructureStatisticsDTO = Field(default_factory=DEXStructureStatisticsDTO)
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
