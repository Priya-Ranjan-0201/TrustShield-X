"""Unit tests for Serialization Boundaries (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import FlowBoundaryDTO


def test_serialization_boundary_dto():
    b = FlowBoundaryDTO(
        boundary_type="SERIALIZATION_BOUNDARY",
        source_method="com.bank.JSON.serialize",
        target_method="com.bank.Network.post",
        resolution_status="RESOLVED",
    )

    assert b.boundary_type == "SERIALIZATION_BOUNDARY"
