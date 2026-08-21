import pytest
from app.services.resilience.backup_validation_engine import BackupValidationEngine

def test_backup_poisoning():
    engine = BackupValidationEngine()
    res = engine.validate_backup("bck_poisoned", "ast_pg_primary", checksum_valid=False, is_poisoned=True)
    assert res.integrity_status == "POISONED"
    assert res.sandbox_tested is False
