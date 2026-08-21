"""Unit tests for Android Component Intelligence Engine (Phase 3.7 Part 1A.9)."""

import pytest
from app.services.component_intelligence import ComponentIntelligenceService
from app.schemas.manifest_intelligence_models import (
    ManifestIntelligenceDTO,
    ComponentDTO,
    ComponentType,
    IntentFilterDTO,
)
from app.schemas.component_intelligence_models import ExportStatus


def test_analyze_components_flow():
    service = ComponentIntelligenceService()
    manifest_dto = ManifestIntelligenceDTO(
        package_name="com.test.app",
        activities=[
            ComponentDTO(
                name=".MainActivity",
                component_type=ComponentType.ACTIVITY,
                exported=None,  # Implicit export via launcher intent filter
                intent_filters=[
                    IntentFilterDTO(
                        actions=["android.intent.action.MAIN"],
                        categories=["android.intent.category.LAUNCHER"],
                    )
                ],
            )
        ],
        services=[
            ComponentDTO(
                name=".MyService",
                component_type=ComponentType.SERVICE,
                exported=False,
            )
        ],
    )

    result = service.analyze_components(manifest_dto)

    assert result.statistics.total_components == 2
    assert result.statistics.activities_count == 1
    assert result.statistics.services_count == 1
    assert result.statistics.launcher_activities_count == 1

    # Check Export Status resolution
    activity = result.components[0]
    assert activity.exported_status == ExportStatus.IMPLICIT_EXPORTED
    assert activity.is_launcher is True

    service_comp = result.components[1]
    assert service_comp.exported_status == ExportStatus.NON_EXPORTED
