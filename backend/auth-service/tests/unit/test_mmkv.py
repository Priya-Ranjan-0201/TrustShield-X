"""Unit tests for MMKV High-Performance Key-Value Storage (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseInstanceDTO


def test_mmkv_dto():
    mmkv = DatabaseInstanceDTO(
        database_name="mmkv_store",
        database_type="MMKV",
        file_path="/data/data/com.bank/files/mmkv",
        is_encrypted=True,
    )

    assert mmkv.database_type == "MMKV"
    assert mmkv.is_encrypted is True
