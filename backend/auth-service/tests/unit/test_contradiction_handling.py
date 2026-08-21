"""Unit tests for Contradiction Penalty Evaluation (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskContradictionDTO


def test_risk_contradiction_dto():
    cntr = RiskContradictionDTO(
        contradiction_id="cntr_1",
        description="Encrypted vs Cleartext claim",
        uncertainty_penalty=2.0,
    )

    assert cntr.uncertainty_penalty == 2.0
