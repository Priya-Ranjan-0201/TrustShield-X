"""Unit tests for Native Filesystem APIs (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageOperationDTO


def test_native_filesystem_dto():
    op = StorageOperationDTO(
        caller_method="libnative.so -> Java_com_bank_Native_openFile",
        operation_type="OPEN",
        target_path="/data/data/com.bank/files/native.dat",
        framework="Native C/C++ POSIX IO",
    )

    assert op.framework == "Native C/C++ POSIX IO"
