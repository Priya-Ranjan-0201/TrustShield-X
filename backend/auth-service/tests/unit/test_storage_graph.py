"""Unit tests for Storage Graph Construction (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import StorageGraphEdgeDTO


def test_storage_graph_dto():
    edge = StorageGraphEdgeDTO(
        source_node="com.bank.Auth.save",
        target_node="/data/data/com.bank/shared_prefs/user_session.xml",
        relationship="STORES_DATA",
    )

    assert edge.relationship == "STORES_DATA"
