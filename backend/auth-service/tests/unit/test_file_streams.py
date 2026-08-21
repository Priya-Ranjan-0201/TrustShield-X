"""Unit tests for File Stream Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import FileOperationDTO


def test_file_stream_dto():
    fop = FileOperationDTO(
        caller_method="com.bank.Stream.read",
        file_path="/data/data/com.bank/files/data.bin",
        action="STREAM",
        stream_class="java.io.DataInputStream",
    )

    assert fop.action == "STREAM"
    assert fop.stream_class == "java.io.DataInputStream"
