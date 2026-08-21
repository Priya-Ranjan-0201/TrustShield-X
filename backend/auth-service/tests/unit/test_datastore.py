"""Unit tests for Android DataStore Detection (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DataStoreDTO


def test_datastore_dto():
    ds = DataStoreDTO(
        caller_method="com.bank.Settings.update",
        datastore_name="settings.preferences_pb",
        datastore_type="PROTO",
        key_or_message="UserSettingsProto",
        operation="WRITE",
    )

    assert ds.datastore_type == "PROTO"
    assert ds.operation == "WRITE"
