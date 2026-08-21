"""Unit tests for Obfuscated Storage Reconstruction (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageLocationDTO


def test_obfuscated_storage_dto():
    loc = StorageLocationDTO(
        location_path="/data/data/com.bank/files/a/b/c.dat",
        location_type="INTERNAL_FILES",
        access_permission="READ_WRITE",
        is_encrypted=False,
        source_method="a.b.c.a",
    )

    assert loc.source_method == "a.b.c.a"
