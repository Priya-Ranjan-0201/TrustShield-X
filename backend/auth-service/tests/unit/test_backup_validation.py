import pytest
from app.services.resilience.backup_validation_engine import BackupValidationEngine

def test_backup_validation():
    engine = BackupValidationEngine()
    res = engine.validate_backup("bck_test_1", "ast_pg_primary", checksum_valid=True, schema_valid=True)
    assert res.integrity_status == "VERIFIED"
    assert res.sandbox_tested is True
