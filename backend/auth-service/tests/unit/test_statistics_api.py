"""Unit tests for API Statistics & Exporters (Phase 3.7 Part 1A.16)."""

import pytest
from app.schemas.api_intelligence_models import APIStatisticsDTO


def test_api_statistics_dto():
    stats = APIStatisticsDTO(total_apis=140, unique_frameworks=4, most_used_capability="NETWORK")

    assert stats.total_apis == 140
    assert stats.unique_frameworks == 4
    assert stats.most_used_capability == "NETWORK"
