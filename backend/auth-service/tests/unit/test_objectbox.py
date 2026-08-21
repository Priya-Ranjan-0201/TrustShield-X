"""Unit tests for ObjectBox Database Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseInstanceDTO


def test_objectbox_dto():
    ob = DatabaseInstanceDTO(
        database_name="objectbox",
        database_type="OBJECTBOX",
        file_path="/data/data/com.bank/files/objectbox",
        is_encrypted=False,
    )

    assert ob.database_type == "OBJECTBOX"
