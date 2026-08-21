"""Unit tests for File Operations Inspection (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import FileOperationDTO


def test_file_operation_dto():
    fop = FileOperationDTO(
        caller_method="com.bank.FileIO.write",
        file_path="/data/data/com.bank/files/cache.bin",
        action="WRITE",
        stream_class="java.io.FileOutputStream",
    )

    assert fop.action == "WRITE"
    assert fop.stream_class == "java.io.FileOutputStream"
