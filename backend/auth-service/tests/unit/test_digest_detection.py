"""Unit tests for MessageDigest & Hash Detection (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import CryptoAlgorithmDTO, CryptoOperationDTO


def test_digest_operation():
    op = CryptoOperationDTO(caller_method="com.bank.Utils.hashPayload", operation_type="HASH", api_used="java.security.MessageDigest", algorithm="SHA-256")

    assert op.operation_type == "HASH"
    assert op.algorithm == "SHA-256"
