"""Unit tests for Risk Aggregation Frontend Contract DTOs (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskCardDTO, RiskSummaryDTO


def test_risk_frontend_contract_dtos():
    card = RiskCardDTO(
        card_id="card_1",
        category="NETWORK_THREAT",
        score=15.0,
        risk_band="TRUSTED",
    )
    summary = RiskSummaryDTO(
        title="Final Assessment",
        risk_score=25.0,
        risk_band="LOW_RISK",
    )

    assert card.category == "NETWORK_THREAT"
    assert summary.risk_score == 25.0
