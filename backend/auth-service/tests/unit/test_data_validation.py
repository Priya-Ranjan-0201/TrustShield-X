import pytest
from app.services.resilience.backup_validation_engine import BackupValidationEngine

def test_data_validation():
    engine = BackupValidationEngine()
    res = engine.validate_backup("bck_data_1", "ast_pg_primary", checksum_valid=True, schema_valid=True)
    assert res.record_count > 0
    assert res.schema_compatible is True
