"""Unit tests for Crypto + Network Correlation (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_crypto_network_dto():
    f = BehaviorFindingDTO(
        finding_id="cn_1",
        finding_type="TLS_PROTECTED_NETWORK",
        category="NETWORK_ENCRYPTION",
        evidence_strength="DIRECT",
        summary="TLS socket connection configured",
    )

    assert f.finding_type == "TLS_PROTECTED_NETWORK"
