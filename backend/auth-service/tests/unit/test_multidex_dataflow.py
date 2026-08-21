"""Unit tests for Multi-DEX Dataflow Intelligence Analysis (Phase 3.9 Part 1A.21)."""

import pytest
from app.services.dataflow_intelligence_service import DataflowIntelligenceService
from app.schemas.api_intelligence_models import APIIntelligenceResultDTO, APIUsageDTO


def test_multidex_dataflow_analysis():
    service = DataflowIntelligenceService()
    api_dto = APIIntelligenceResultDTO(
        api_usage=[
            APIUsageDTO(
                caller_method="com.bank.secondary.Location.get",
                api_canonical_id="android.location.LocationManager.getLastKnownLocation()",
            ),
            APIUsageDTO(
                caller_method="com.bank.tertiary.Net.send",
                api_canonical_id="okhttp3.OkHttpClient.newCall()",
            ),
        ]
    )

    res = service.analyze_dataflow(api_intelligence_dto=api_dto)

    assert len(res.sources) >= 1
    assert len(res.sinks) >= 1
    assert res.json_export is not None
    assert res.csv_export is not None
    assert res.dot_export is not None
    assert res.mermaid_export is not None
