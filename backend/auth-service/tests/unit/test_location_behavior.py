"""Unit tests for Location Behavior Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.services.behavioral_correlation_service import BehavioralCorrelationService
from app.schemas.permission_intelligence_models import PermissionIntelligenceResultDTO, EnrichedPermissionDTO
from app.schemas.api_intelligence_models import APIIntelligenceResultDTO, APIUsageDTO


def test_location_behavior_correlation():
    service = BehavioralCorrelationService()
    perm_dto = PermissionIntelligenceResultDTO(
        permissions=[EnrichedPermissionDTO(permission_name="android.permission.ACCESS_FINE_LOCATION", category="LOCATION", protection_level="DANGEROUS")]
    )
    api_dto = APIIntelligenceResultDTO(
        api_usage=[APIUsageDTO(caller_method="com.bank.Loc.get", api_canonical_id="android.location.LocationManager.getLastKnownLocation")]
    )

    res = service.correlate_behavior(
        permission_intelligence_dto=perm_dto,
        api_intelligence_dto=api_dto,
    )

    assert any(f.finding_type == "LOCATION_COLLECTION" for f in res.findings)
