"""Unit tests for Intent & Deep Link Intelligence Engine (Phase 3.7 Part 1A.10)."""

import pytest
from app.services.intent_intelligence import IntentIntelligenceService
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
)


def test_analyze_intents_flow():
    service = IntentIntelligenceService()
    manifest_dto = ManifestIntelligenceDTO(
        package_name="com.test.app",
        activities=[
            ComponentDTO(
                name=".MainActivity",
                component_type=ComponentType.ACTIVITY,
                exported=True,
                intent_filters=[
                    IntentFilterDTO(
                        actions=["android.intent.action.MAIN", "android.intent.action.VIEW"],
                        categories=["android.intent.category.LAUNCHER", "android.intent.category.BROWSABLE"],
                        schemes=["https"],
                        hosts=["example.com"],
                    )
                ],
            )
        ],
    )

    result = service.analyze_intents(manifest_dto)

    assert result.statistics.total_intent_filters == 1
    assert result.statistics.total_actions == 2
    assert result.statistics.total_categories == 2
    assert result.statistics.total_deep_links == 1
    assert result.statistics.launcher_count == 1
    assert result.statistics.browsable_count == 1
    assert result.statistics.app_links_count == 1
    assert result.statistics.https_links_count == 1
    assert len(result.navigation_nodes) == 2
