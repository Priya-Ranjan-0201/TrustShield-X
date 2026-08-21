"""Unit tests for Crypto + Storage Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_crypto_storage_dto():
    f = BehaviorFindingDTO(
        finding_id="cs_1",
        finding_type="ENCRYPTED_LOCAL_STORAGE",
        category="LOCAL_DATA_ENCRYPTION",
        evidence_strength="DIRECT",
        summary="EncryptedSharedPreferences detected",
    )

    assert f.finding_type == "ENCRYPTED_LOCAL_STORAGE"
