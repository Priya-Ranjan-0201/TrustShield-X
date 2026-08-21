"""Unit tests for DEX Structure Intelligence Parser (Phase 3.7 Part 1A.13)."""

import struct
import pytest
from app.services.dex_structure_service import DEXStructureService


def test_parse_dex_header_valid():
    # Build 112-byte mock DEX header
    hdr_bytes = bytearray(112)
    hdr_bytes[0:8] = b"dex\n035\x00"
    struct.pack_into("<I", hdr_bytes, 8, 0x12345678)  # checksum
    struct.pack_into("<I", hdr_bytes, 32, 1024)  # file size
    struct.pack_into("<I", hdr_bytes, 36, 112)  # header size

    service = DEXStructureService()
    header = service.parse_dex_header(bytes(hdr_bytes))

    assert header is not None
    assert header.dex_version == "035"
    assert header.checksum == 0x12345678
    assert header.file_size == 1024
    assert header.header_size == 112
