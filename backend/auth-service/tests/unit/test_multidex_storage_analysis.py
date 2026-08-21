"""Unit tests for Multi-DEX Storage Intelligence Analysis (Phase 3.9 Part 1A.20)."""

import pytest
from app.services.data_filesystem_intelligence_service import DataFilesystemIntelligenceService
from app.schemas.api_intelligence_models import APIIntelligenceResultDTO, APIUsageDTO


def test_multidex_storage_analysis():
    service = DataFilesystemIntelligenceService()
    api_dto = APIIntelligenceResultDTO(
        api_usage=[
            APIUsageDTO(
                caller_method="com.bank.secondary.Storage.init",
                api_canonical_id="android.content.Context.getFilesDir()Ljava/io/File;",
            ),
            APIUsageDTO(
                caller_method="com.bank.tertiary.DB.open",
                api_canonical_id="android.database.sqlite.SQLiteDatabase.openOrCreateDatabase()",
            ),
        ]
    )

    res = service.analyze_storage(api_intelligence_dto=api_dto)

    assert len(res.locations) >= 1
    assert res.metrics.locations_count >= 1
    assert res.json_export is not None
    assert res.csv_export is not None
    assert res.dot_export is not None
    assert res.mermaid_export is not None
