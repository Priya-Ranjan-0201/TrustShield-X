"""Unit tests for Permission + API Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.services.behavioral_correlation_service import BehavioralCorrelationService
from app.schemas.permission_intelligence_models import PermissionIntelligenceResultDTO, EnrichedPermissionDTO


def test_permission_declared_only():
    service = BehavioralCorrelationService()
    perm_dto = PermissionIntelligenceResultDTO(
        permissions=[EnrichedPermissionDTO(permission_name="android.permission.READ_SMS", category="SMS", protection_level="DANGEROUS")]
    )

    res = service.correlate_behavior(permission_intelligence_dto=perm_dto)

    assert any(f.finding_type == "DECLARED_ONLY_PERMISSION" for f in res.findings)
