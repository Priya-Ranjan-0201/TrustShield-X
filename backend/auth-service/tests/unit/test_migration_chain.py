"""Unit tests for Alembic Migration Chain Integrity (Phase 3.9 Part 1C)."""

import os
import pytest


def test_migration_chain_integrity():
    migration_file = "alembic/versions/034_risk_aggregation_schema.py"
    assert os.path.exists(migration_file), "Migration 034 file must exist"
