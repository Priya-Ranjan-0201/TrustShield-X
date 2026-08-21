"""Unit tests for Database Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_database_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="user_obj",
        target_node_id="db_table_users",
        edge_type="DATABASE_INSERT",
        caller_method="com.bank.DAO.insert",
    )

    assert edge.edge_type == "DATABASE_INSERT"
