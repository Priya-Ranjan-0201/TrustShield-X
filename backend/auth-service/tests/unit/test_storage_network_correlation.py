"""Unit tests for Storage + Network Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_storage_network_dto():
    f = BehaviorFindingDTO(
        finding_id="sn_1",
        finding_type="STORAGE_TO_NETWORK",
        category="DATA_TRANSMISSION",
        evidence_strength="DIRECT",
        summary="SharedPreferences loaded and sent over HTTPS",
    )

    assert f.finding_type == "STORAGE_TO_NETWORK"
