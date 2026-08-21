import pytest
from app.services.resilience.backup_validation_engine import BackupValidationEngine

def test_restore_security():
    engine = BackupValidationEngine()
    res = engine.validate_backup("bck_corrupt", "ast_pg_primary", checksum_valid=False)
    assert res.integrity_status == "CORRUPTED"
