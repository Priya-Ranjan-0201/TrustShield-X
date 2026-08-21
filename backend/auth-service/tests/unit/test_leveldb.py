"""Unit tests for LevelDB / RocksDB Intelligence (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DatabaseInstanceDTO


def test_leveldb_dto():
    ldb = DatabaseInstanceDTO(
        database_name="leveldb_store",
        database_type="LEVELDB",
        file_path="/data/data/com.bank/files/leveldb",
    )

    assert ldb.database_type == "LEVELDB"
