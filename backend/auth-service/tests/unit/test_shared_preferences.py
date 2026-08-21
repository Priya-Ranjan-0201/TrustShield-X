"""Unit tests for SharedPreferences Analysis (Phase 3.9 Part 1A.20)."""

import pytest
from app.schemas.data_filesystem_models import SharedPreferenceDTO


def test_shared_preference_dto():
    pref = SharedPreferenceDTO(
        caller_method="com.bank.Auth.saveToken",
        preference_file="user_session",
        key_name="auth_token",
        value_type="STRING",
        operation="WRITE",
        is_encrypted=True,
    )

    assert pref.preference_file == "user_session"
    assert pref.key_name == "auth_token"
    assert pref.is_encrypted is True
