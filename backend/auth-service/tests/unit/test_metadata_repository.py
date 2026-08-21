"""Unit tests for Async APK Metadata Repository (Phase 3.7 Part 1A.11)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.apk_metadata_repository import APKMetadataRepository
from app.schemas.apk_metadata_intelligence_models import (
    APKMetadataIntelligenceResultDTO,
    VersionIntelligenceDTO,
    SDKProfileDTO,
    ApplicationFlagsDTO,
    ResourceReferencesDTO,
    InstallLocation,
)


@pytest.mark.asyncio
async def test_metadata_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = APKMetadataRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = APKMetadataIntelligenceResultDTO(
        package_name="com.test.app",
        version_info=VersionIntelligenceDTO(version_name="1.0.0", version_code=100),
        sdk_profile=SDKProfileDTO(min_sdk=21, target_sdk=33),
        install_location=InstallLocation.AUTO,
        app_flags=ApplicationFlagsDTO(is_debuggable=False),
        resources=ResourceReferencesDTO(app_label="TestApp"),
    )

    model = await repo.save_full_metadata_intelligence(scan_id, dto)
    assert model.scan_id == scan_id
    assert model.package_name == "com.test.app"
    assert db_mock.add.called
    assert db_mock.commit.called
