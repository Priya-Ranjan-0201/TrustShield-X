"""Unit tests for Native Library Scanner (Phase 3.7 Part 1A Message 2)."""

import pytest
from app.services.native_library_scanner import NativeLibraryScanner


def test_native_library_scanner():
    scanner = NativeLibraryScanner()
    entries = [
        ("lib/arm64-v8a/libnative.so", b"\x7fELF" + b"\x00" * 1000),
        ("lib/armeabi-v7a/libnative.so", b"\x7fELF" + b"\x00" * 800),
        ("lib/x86_64/libnative.so", b"\x7fELF" + b"\x00" * 1200),
    ]

    res = scanner.scan_native_libraries(entries)
    assert res.library_count == 3
    assert "arm64-v8a" in res.architectures_present
    assert "armeabi-v7a" in res.architectures_present
    assert "x86_64" in res.architectures_present
    assert res.largest_library_bytes == 1204
    assert res.largest_library_name == "libnative.so"
