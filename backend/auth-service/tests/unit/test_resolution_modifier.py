"""Unit tests for Evidence Resolution Modifiers (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskFactorDTO


def test_resolution_modifier():
    factor = RiskFactorDTO(
        factor_id="f_res",
        category="DATA_EXFILTRATION",
        name="Resolved Exfiltration Path",
        description="Desc",
        base_contribution=25.0,
        final_contribution=25.0,
        confidence="HIGH",
        evidence_sufficiency="SUFFICIENT",
        reason="Reason",
    )

    assert factor.base_contribution == 25.0
