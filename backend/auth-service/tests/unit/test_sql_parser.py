"""Unit tests for SQL Parsing Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseQueryDTO


def test_sql_parser_dto():
    q = DatabaseQueryDTO(
        caller_method="com.bank.DAO.insertUser",
        query_type="INSERT",
        raw_sql="INSERT INTO users (id, name) VALUES (?, ?)",
        target_table="users",
    )

    assert q.query_type == "INSERT"
    assert q.target_table == "users"
