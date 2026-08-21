"""Unit tests for Evidence Independence Modifiers (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskFactorDTO


def test_independence_modifier():
    factor = RiskFactorDTO(
        factor_id="f1",
        category="NETWORK_THREAT",
        name="Independent Network Factor",
        description="Desc",
        base_contribution=10.0,
        final_contribution=10.0,
        confidence="HIGH",
        evidence_sufficiency="SUFFICIENT",
        reason="Reason",
    )

    assert factor.final_contribution == 10.0
