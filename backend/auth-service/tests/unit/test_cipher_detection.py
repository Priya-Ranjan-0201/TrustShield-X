"""Unit tests for Cipher & Algorithm Detection (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import CryptoAlgorithmDTO, CryptoOperationDTO


def test_crypto_algorithm_and_operation_dtos():
    alg = CryptoAlgorithmDTO(algorithm_name="AES-256-GCM", family="SYMMETRIC", key_size=256, mode="GCM", padding="NoPadding")
    op = CryptoOperationDTO(caller_method="com.bank.Crypto.encrypt", operation_type="ENCRYPT", api_used="javax.crypto.Cipher", algorithm="AES-256-GCM")

    assert alg.algorithm_name == "AES-256-GCM"
    assert alg.key_size == 256
    assert alg.mode == "GCM"
    assert op.operation_type == "ENCRYPT"
    assert op.api_used == "javax.crypto.Cipher"
