"""Unit tests for Serialization Operations (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import SerializationOperationDTO


def test_serialization_dto():
    ser = SerializationOperationDTO(
        caller_method="com.bank.JSON.parse",
        format="GSON",
        direction="DESERIALIZE",
        data_model_class="com.bank.model.UserResponse",
    )

    assert ser.format == "GSON"
    assert ser.direction == "DESERIALIZE"
