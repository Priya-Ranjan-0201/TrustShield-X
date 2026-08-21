"""Unit tests for Permission Intelligence Normalization Engine (Phase 3.7 Part 1A.8)."""

import pytest
from app.services.permission_intelligence import PermissionIntelligenceService
from app.schemas.manifest_intelligence_models import PermissionRefDTO


def test_enrich_permissions_flow():
    service = PermissionIntelligenceService()
    raw_perms = [
        PermissionRefDTO(name="android.permission.CAMERA"),
        PermissionRefDTO(name="android.permission.INTERNET"),
        PermissionRefDTO(name="com.custom.app.MY_PERM"),
        PermissionRefDTO(name="android.permission.CAMERA"),  # Duplicate to test deduplication
    ]

    result = service.enrich_permissions(raw_perms)

    assert result.statistics.total_permissions == 3
    assert result.statistics.dangerous_count == 1
    assert result.statistics.normal_count == 1
    assert result.statistics.custom_count == 1
    assert result.knowledge_base_hits == 2
    assert len(result.permissions) == 3
