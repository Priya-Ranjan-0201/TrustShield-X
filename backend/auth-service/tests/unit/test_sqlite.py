"""Unit tests for SQLite Database Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseInstanceDTO, DatabaseQueryDTO


def test_sqlite_dtos():
    db_inst = DatabaseInstanceDTO(
        database_name="app_vault.db",
        database_type="SQLITE",
        file_path="/data/data/com.bank/databases/app_vault.db",
        is_encrypted=False,
    )
    query = DatabaseQueryDTO(
        caller_method="com.bank.DB.getUsers",
        query_type="SELECT",
        raw_sql="SELECT * FROM users",
        target_table="users",
    )

    assert db_inst.database_name == "app_vault.db"
    assert query.query_type == "SELECT"
