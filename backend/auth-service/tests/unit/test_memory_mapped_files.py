"""Unit tests for Memory-Mapped Files (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import FileOperationDTO


def test_mmap_dto():
    fop = FileOperationDTO(
        caller_method="com.bank.MMap.map",
        file_path="/data/data/com.bank/files/large_db.bin",
        action="MAP_MEMORY",
        stream_class="java.nio.MappedByteBuffer",
    )

    assert fop.action == "MAP_MEMORY"
    assert fop.stream_class == "java.nio.MappedByteBuffer"
