"""Unit tests for External Storage Inspection (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageLocationDTO, FileSystemObjectDTO


def test_external_storage_dtos():
    loc = StorageLocationDTO(
        location_path="/sdcard/Android/data/com.bank/files",
        location_type="EXTERNAL_FILES",
        access_permission="READ_WRITE",
        is_encrypted=False,
        source_method="com.bank.Storage.initExt",
    )
    fso = FileSystemObjectDTO(
        path="/sdcard/download/statement.pdf",
        file_type="FILE",
        mime_type="application/pdf",
        is_external=True,
    )

    assert loc.location_type == "EXTERNAL_FILES"
    assert fso.is_external is True
