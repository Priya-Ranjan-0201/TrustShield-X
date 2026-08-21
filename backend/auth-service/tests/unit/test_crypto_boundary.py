"""Unit tests for Cryptographic Boundaries (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import FlowBoundaryDTO


def test_crypto_boundary_dto():
    b = FlowBoundaryDTO(
        boundary_type="CRYPTOGRAPHIC_BOUNDARY",
        source_method="com.bank.Crypto.encrypt",
        target_method="com.bank.Network.send",
        resolution_status="RESOLVED",
    )

    assert b.boundary_type == "CRYPTOGRAPHIC_BOUNDARY"
