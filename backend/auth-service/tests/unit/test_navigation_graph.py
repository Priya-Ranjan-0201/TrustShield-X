"""Unit tests for Navigation Graph Builder (Phase 3.7 Part 1A.10)."""

import pytest
from app.services.intent_intelligence import IntentIntelligenceService
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
)


def test_navigation_graph_construction():
    service = IntentIntelligenceService()
    manifest_dto = ManifestIntelligenceDTO(
        package_name="com.nav.app",
        activities=[
            ComponentDTO(
                name=".DeepLinkActivity",
                component_type=ComponentType.ACTIVITY,
                exported=True,
                intent_filters=[
                    IntentFilterDTO(
                        actions=["android.intent.action.VIEW"],
                        categories=["android.intent.category.BROWSABLE", "android.intent.category.DEFAULT"],
                        schemes=["https"],
                        hosts=["pay.trustshield.com"],
                    )
                ],
            )
        ],
    )

    result = service.analyze_intents(manifest_dto)
    assert len(result.navigation_nodes) == 1
    node = result.navigation_nodes[0]
    assert node.source_component == "EXTERNAL_INTENT"
    assert node.intent_action == "android.intent.action.VIEW"
    assert node.target_scheme == "https"
    assert node.target_host == "pay.trustshield.com"
    assert node.destination_component == ".DeepLinkActivity"
