"""Unit tests for DEX Discovery Engine (Phase 3.7 Part 1A Message 2)."""

import struct
import pytest
from app.services.dex_scanner import DEXScanner


def test_dex_scanner_multi_dex():
    scanner = DEXScanner()

    # Create dummy DEX header bytes
    # Offset 0x58 -> method_ids_size (100)
    # Offset 0x60 -> class_defs_size (25)
    dex1 = bytearray(b"dex\n035\x00" + b"\x00" * 0x80)
    struct.pack_into("<I", dex1, 0x58, 100)
    struct.pack_into("<I", dex1, 0x60, 25)

    dex2 = bytearray(b"dex\n035\x00" + b"\x00" * 0x80)
    struct.pack_into("<I", dex2, 0x58, 150)
    struct.pack_into("<I", dex2, 0x60, 40)

    entries = [
        ("classes.dex", bytes(dex1)),
        ("classes2.dex", bytes(dex2)),
    ]

    res = scanner.scan_dex_entries(entries)
    assert res.total_dex_files == 2
    assert len(res.dex_files) == 2
    assert res.dex_files[0].filename == "classes.dex"
    assert res.dex_files[0].class_count == 25
    assert res.dex_files[0].method_count == 100
    assert res.dex_files[1].filename == "classes2.dex"
    assert res.dex_files[1].class_count == 40
    assert res.dex_files[1].method_count == 150


def test_dex_scanner_corrupt_header_graceful():
    scanner = DEXScanner()
    corrupt_dex = b"corrupted non-dex data"
    entries = [("classes.dex", corrupt_dex)]

    res = scanner.scan_dex_entries(entries)
    assert res.total_dex_files == 1
    assert res.dex_files[0].class_count == 0
    assert res.dex_files[0].method_count == 0
