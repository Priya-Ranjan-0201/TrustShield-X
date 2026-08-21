"""Unit tests for Semantic Version Dissection (Phase 3.7 Part 1A.11)."""

import pytest
from app.services.apk_metadata_intelligence import APKMetadataIntelligenceService


def test_parse_version_name_semantic():
    service = APKMetadataIntelligenceService()
    v = service.parse_version_name("2.4.1", 20401)

    assert v.version_name == "2.4.1"
    assert v.version_code == 20401
    assert v.major == 2
    assert v.minor == 4
    assert v.patch == 1
    assert v.build is None


def test_parse_version_name_four_parts():
    service = APKMetadataIntelligenceService()
    v = service.parse_version_name("3.0.12.99", 30012)

    assert v.major == 3
    assert v.minor == 0
    assert v.patch == 12
    assert v.build == 99
