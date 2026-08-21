"""Unit tests for Alembic Migration 011 (Phase 3.7 Part 1A Message 3A)."""

import pytest
from alembic.config import Config
from alembic import command


def test_migration_011_structure():
    import importlib.util

    spec = importlib.util.spec_from_file_location("migration_011", "alembic/versions/011_apk_infrastructure_schema.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.revision == "011"
    assert module.down_revision == "010"
    assert hasattr(module, "upgrade")
    assert hasattr(module, "downgrade")
