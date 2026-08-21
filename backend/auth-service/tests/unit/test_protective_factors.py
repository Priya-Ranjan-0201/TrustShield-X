"""Unit tests for Protective Control Factors (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskProtectiveFactorDTO


def test_protective_factor_dto():
    prot = RiskProtectiveFactorDTO(
        protective_id="prot_1",
        description="Certificate pinning active",
        reduction_amount=5.0,
    )

    assert prot.reduction_amount == 5.0
