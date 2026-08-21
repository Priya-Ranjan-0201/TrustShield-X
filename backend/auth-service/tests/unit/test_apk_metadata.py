"""Unit tests for APK Metadata & Package Intelligence Engine (Phase 3.7 Part 1A.11)."""

import pytest
from app.services.apk_metadata_intelligence import APKMetadataIntelligenceService
from app.schemas.manifest_intelligence_models import ManifestIntelligenceDTO
from app.schemas.apk_metadata_intelligence_models import InstallLocation


def test_analyze_metadata_flow():
    service = APKMetadataIntelligenceService()
    manifest_dto = ManifestIntelligenceDTO(
        package_name="com.example.bank",
        version_code=10203,
        version_name="1.2.3.400",
        min_sdk=24,
        target_sdk=33,
        compile_sdk=33,
        install_location="internalOnly",
        application_label="SecureBank",
        is_debuggable=False,
        uses_cleartext_traffic=False,
    )

    result = service.analyze_metadata(manifest_dto)

    assert result.package_name == "com.example.bank"
    assert result.version_info.version_name == "1.2.3.400"
    assert result.version_info.major == 1
    assert result.version_info.minor == 2
    assert result.version_info.patch == 3
    assert result.version_info.build == 400
    assert result.sdk_profile.target_sdk == 33
    assert result.sdk_profile.generation_name == "Android 13 (Tiramisu)"
    assert result.install_location == InstallLocation.INTERNAL
    assert result.resources.app_label == "SecureBank"
