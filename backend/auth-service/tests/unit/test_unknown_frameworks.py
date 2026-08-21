"""Unit tests for Unknown Frameworks & Full API Intelligence Pipeline (Phase 3.7 Part 1A.16)."""

import pytest
from app.services.api_intelligence_service import APIIntelligenceService


def test_full_api_intelligence_service():
    service = APIIntelligenceService()

    class MockCallEdge:
        caller_method = "com.example.bank.Login.submit"
        callee_method = "Landroid/net/ConnectivityManager;->getActiveNetworkInfo()Landroid/net/NetworkInfo;"
        offset = 12

    class MockProgramGraphDTO:
        call_graph_edges = [MockCallEdge()]

    result = service.analyze_apis(program_graph_dto=MockProgramGraphDTO())

    assert len(result.api_catalog) == 1
    assert result.api_catalog[0].canonical_id == "android.net.ConnectivityManager.getActiveNetworkInfo"
    assert len(result.capabilities) == 1
    assert result.capabilities[0].capability.value == "NETWORK"
    assert result.json_export is not None
    assert result.csv_export is not None
