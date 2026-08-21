"""Unit tests for Realm Database Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseInstanceDTO


def test_realm_dto():
    realm = DatabaseInstanceDTO(
        database_name="default.realm",
        database_type="REALM",
        file_path="/data/data/com.bank/files/default.realm",
        is_encrypted=True,
    )

    assert realm.database_type == "REALM"
    assert realm.is_encrypted is True
