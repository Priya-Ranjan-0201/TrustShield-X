"""Unit tests for Mitigating Factor Reduction (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskMitigationDTO


def test_risk_mitigation_dto():
    mit = RiskMitigationDTO(
        mitigation_id="mit_1",
        description="Data encrypted prior to storage",
        reduction_amount=5.0,
    )

    assert mit.reduction_amount == 5.0
