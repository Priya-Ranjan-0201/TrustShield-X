"""Unit tests for Compression Operations (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import CompressionOperationDTO


def test_compression_dto():
    comp = CompressionOperationDTO(
        caller_method="com.bank.Zip.unzip",
        algorithm="ZIP",
        operation="DECOMPRESS",
    )

    assert comp.algorithm == "ZIP"
    assert comp.operation == "DECOMPRESS"
