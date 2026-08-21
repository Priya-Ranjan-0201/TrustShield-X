"""Unit tests for SecureRandom Inspection (Phase 3.7 Part 1A.18)."""

import pytest
from app.schemas.cryptography_models import SecureRandomUsageDTO


def test_secure_random_dto():
    rng = SecureRandomUsageDTO(caller_method="com.bank.Crypto.genIV", rng_class="java.security.SecureRandom", has_seed=False)

    assert rng.caller_method == "com.bank.Crypto.genIV"
    assert rng.rng_class == "java.security.SecureRandom"
    assert rng.has_seed is False
