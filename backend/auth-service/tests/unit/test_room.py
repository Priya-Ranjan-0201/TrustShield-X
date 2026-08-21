"""Unit tests for Room ORM Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseTableDTO, DatabaseColumnDTO


def test_room_dtos():
    tbl = DatabaseTableDTO(
        database_name="app_room.db",
        table_name="accounts",
        primary_key_column="account_id",
        columns_count=3,
    )
    col = DatabaseColumnDTO(
        table_name="accounts",
        column_name="balance",
        data_type="REAL",
        is_primary_key=False,
    )

    assert tbl.table_name == "accounts"
    assert col.data_type == "REAL"
