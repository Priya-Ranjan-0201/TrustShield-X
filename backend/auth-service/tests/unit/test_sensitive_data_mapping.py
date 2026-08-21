"""Unit tests for Sensitive Data Location Mapping (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import DataSensitivityDTO


def test_sensitive_data_dto():
    sens = DataSensitivityDTO(
        category="CREDENTIALS",
        storage_type="SHARED_PREFERENCES",
        location_identifier="auth_prefs.xml -> password",
        source_method="com.bank.Auth.save",
        redaction_status="REDACTED",
    )

    assert sens.category == "CREDENTIALS"
    assert sens.redaction_status == "REDACTED"
