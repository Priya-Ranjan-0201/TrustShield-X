"""Unit tests for Digital Signature Detection (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import DigitalSignatureDTO


def test_digital_signature_dto():
    sig = DigitalSignatureDTO(caller_method="com.bank.Auth.signJWT", signature_algorithm="SHA256withRSA", operation="SIGN")

    assert sig.caller_method == "com.bank.Auth.signJWT"
    assert sig.signature_algorithm == "SHA256withRSA"
    assert sig.operation == "SIGN"
