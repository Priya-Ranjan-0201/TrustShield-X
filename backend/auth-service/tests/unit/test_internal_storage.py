"""Unit tests for Internal Storage Detection (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageLocationDTO


def test_internal_storage_dto():
    loc = StorageLocationDTO(
        location_path="/data/data/com.bank/files",
        location_type="INTERNAL_FILES",
        access_permission="READ_WRITE",
        is_encrypted=False,
        source_method="com.bank.Storage.init",
    )

    assert loc.location_path == "/data/data/com.bank/files"
    assert loc.location_type == "INTERNAL_FILES"
    assert loc.is_encrypted is False
