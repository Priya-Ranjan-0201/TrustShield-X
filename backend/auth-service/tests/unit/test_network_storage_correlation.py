"""Unit tests for Network + Storage Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_network_storage_dto():
    f = BehaviorFindingDTO(
        finding_id="ns_1",
        finding_type="NETWORK_TO_STORAGE",
        category="DATA_STORAGE",
        evidence_strength="DIRECT",
        summary="HTTP response stored to SQLite",
    )

    assert f.finding_type == "NETWORK_TO_STORAGE"
