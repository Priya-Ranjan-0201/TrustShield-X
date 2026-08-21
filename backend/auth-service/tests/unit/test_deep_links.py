"""Unit tests for Deep Link Intelligence (Phase 3.7 Part 1A.10)."""

import pytest
from app.services.intent_intelligence import IntentIntelligenceService
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
)


def test_deep_link_extraction_custom_and_app_links():
    service = IntentIntelligenceService()
    manifest_dto = ManifestIntelligenceDTO(
        package_name="com.deeplink.app",
        activities=[
            ComponentDTO(
                name=".CustomSchemeActivity",
                component_type=ComponentType.ACTIVITY,
                exported=True,
                intent_filters=[
                    IntentFilterDTO(
                        actions=["android.intent.action.VIEW"],
                        categories=["android.intent.category.DEFAULT"],
                        schemes=["mycustomapp"],
                        hosts=["auth"],
                    )
                ],
            )
        ],
    )

    result = service.analyze_intents(manifest_dto)
    assert result.statistics.total_deep_links == 1
    assert result.statistics.custom_uri_schemes_count == 1
    dl = result.deep_links[0]
    assert dl.scheme == "mycustomapp"
    assert dl.host == "auth"
    assert dl.is_app_link is False
