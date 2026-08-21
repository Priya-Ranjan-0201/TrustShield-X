"""Unit tests for Encrypted Storage Correlations (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageCryptoRelationshipDTO


def test_encrypted_storage_dto():
    sc = StorageCryptoRelationshipDTO(
        storage_identifier="app_vault.db",
        crypto_operation="SQLCipher",
        key_alias="db_master_key",
    )

    assert sc.storage_identifier == "app_vault.db"
    assert sc.crypto_operation == "SQLCipher"
