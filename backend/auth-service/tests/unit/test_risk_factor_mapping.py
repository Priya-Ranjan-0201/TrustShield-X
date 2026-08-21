"""Unit tests for Risk Factor Mapping (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskFactorDTO


def test_risk_factor_dto():
    factor = RiskFactorDTO(
        factor_id="f1",
        category="CREDENTIAL_THEFT",
        name="Credential Theft",
        description="Description",
        base_contribution=35.0,
        final_contribution=35.0,
        confidence="HIGH",
        evidence_sufficiency="SUFFICIENT",
        reason="Reason",
    )

    assert factor.category == "CREDENTIAL_THEFT"
    assert factor.final_contribution == 35.0
