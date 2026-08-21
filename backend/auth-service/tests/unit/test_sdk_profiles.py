"""Unit tests for SDK Profile Resolution (Phase 3.7 Part 1A.11)."""

import pytest
from app.services.apk_metadata_intelligence import APKMetadataIntelligenceService


def test_resolve_sdk_profile_android13():
    service = APKMetadataIntelligenceService()
    sdk = service.resolve_sdk_profile(min_sdk=21, target_sdk=33, compile_sdk=33)

    assert sdk.min_sdk == 21
    assert sdk.target_sdk == 33
    assert sdk.compile_sdk == 33
    assert sdk.platform_version == "Android 13.0"
    assert sdk.generation_name == "Android 13 (Tiramisu)"


def test_resolve_sdk_profile_android14():
    service = APKMetadataIntelligenceService()
    sdk = service.resolve_sdk_profile(min_sdk=24, target_sdk=34)

    assert sdk.target_sdk == 34
    assert sdk.generation_name == "Android 14 (Upside Down Cake)"
