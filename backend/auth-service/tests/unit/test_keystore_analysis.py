"""Unit tests for Android Keystore Intelligence (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import KeyStoreUsageDTO, CryptoKeyDTO


def test_keystore_dtos():
    ks = KeyStoreUsageDTO(caller_method="com.bank.Crypto.getKey", keystore_type="AndroidKeyStore", operation="GET_KEY")
    key = CryptoKeyDTO(key_alias="alias_master", key_type="SECRET_KEY", provider="AndroidKeyStore", is_hardware_backed=True)

    assert ks.keystore_type == "AndroidKeyStore"
    assert key.key_alias == "alias_master"
    assert key.is_hardware_backed is True
