"""Unit tests for Async Manifest Repository (Phase 3.7 Part 1A.5)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.manifest_repository import ManifestRepository
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    SDKCategory,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
    FeatureDTO,
    LibraryDTO,
)


@pytest.mark.asyncio
async def test_manifest_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = ManifestRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = ManifestIntelligenceDTO(
        package_name="com.test.app",
        version_name="1.0.0",
        version_code=1,
        min_sdk=23,
        target_sdk=33,
        sdk_category=SDKCategory.MODERN,
        activities=[
            ComponentDTO(
                name=".MainActivity",
                component_type=ComponentType.ACTIVITY,
                exported=True,
                intent_filters=[IntentFilterDTO(actions=["android.intent.action.MAIN"])],
            )
        ],
        features=[FeatureDTO(name="android.hardware.camera")],
        libraries=[LibraryDTO(name="org.apache.http.legacy")],
    )

    root_model = await repo.save_full_manifest(scan_id, dto)
    assert root_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
