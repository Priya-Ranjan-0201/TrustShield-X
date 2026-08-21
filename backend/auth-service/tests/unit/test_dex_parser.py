"""Unit tests for DEX & Multi-DEX Intelligence Parser Engine (Phase 3.7 Part 1A.6)."""

import pytest
from app.services.dex_parser import DEXIntelligenceParser, DEXScanner


import struct

SAMPLE_DEX_HEADER_BYTES = (
    b"dex\n035\x00"
    + b"\x00" * 24
    + struct.pack("<IIIIIIIIIIIIIIIIIIII", 112, 112, 0x12345678, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
)


def test_parse_single_dex_header():
    parser = DEXIntelligenceParser()
    dto = parser.parse_single_dex("classes.dex", SAMPLE_DEX_HEADER_BYTES, dex_order=0)

    assert dto.dex_name == "classes.dex"
    assert dto.dex_order == 0
    assert dto.header.magic_version.startswith("dex")
    assert dto.header.header_size == 112


def test_parse_multidex_entries():
    parser = DEXIntelligenceParser()
    dex_entries = [
        ("classes2.dex", SAMPLE_DEX_HEADER_BYTES),
        ("classes.dex", SAMPLE_DEX_HEADER_BYTES),
    ]

    intel_dto = parser.parse_dex_entries(dex_entries)

    assert intel_dto.total_dex_files == 2
    # Verify sorting: classes.dex should be first
    assert intel_dto.dex_files[0].dex_name == "classes.dex"
    assert intel_dto.dex_files[1].dex_name == "classes2.dex"


def test_dex_scanner_compatibility():
    scanner = DEXScanner()
    summary = scanner.scan_dex_entries([("classes.dex", SAMPLE_DEX_HEADER_BYTES)])

    assert summary.total_dex_files == 1
    assert summary.largest_dex_name == "classes.dex"
