"""Unit tests for Temporary Files Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import FileSystemObjectDTO


def test_temp_file_dto():
    fso = FileSystemObjectDTO(
        path="/data/data/com.bank/cache/tmp_12345.tmp",
        file_type="TEMPORARY",
        mime_type="application/octet-stream",
        is_external=False,
    )

    assert fso.file_type == "TEMPORARY"
