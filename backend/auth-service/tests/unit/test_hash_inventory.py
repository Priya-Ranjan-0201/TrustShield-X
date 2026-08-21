"""Unit tests for Binary Fingerprinting & Shannon Entropy (Phase 3.7 Part 1A.12)."""

import pytest
from app.services.apk_binary_inventory import APKBinaryInventoryService


def test_compute_entropy_zero():
    service = APKBinaryInventoryService()
    assert service.compute_entropy(b"") == 0.0


def test_compute_entropy_uniform():
    service = APKBinaryInventoryService()
    # Repeating byte has 0.0 entropy
    assert service.compute_entropy(b"AAAAAAA") == 0.0


def test_generate_fingerprints_hashes():
    service = APKBinaryInventoryService()
    hashes = service.generate_fingerprints(b"test data 12345", crc_val=0x12345678)

    assert len(hashes.sha256) == 64
    assert len(hashes.sha1) == 40
    assert len(hashes.md5) == 32
    assert hashes.crc32 == "12345678"
    assert hashes.entropy > 0.0
