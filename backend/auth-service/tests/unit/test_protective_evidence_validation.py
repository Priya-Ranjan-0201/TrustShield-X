"""Unit tests for Protective Controls Validation (Phase 3.9 Part 1C)."""

import pytest
from app.schemas.risk_aggregation_models import RiskProtectiveFactorDTO


def test_protective_evidence_validation():
    prot = RiskProtectiveFactorDTO(
        protective_id="prot_val",
        description="TLS Pinning Verified",
        reduction_amount=5.0,
    )

    assert prot.reduction_amount == 5.0
