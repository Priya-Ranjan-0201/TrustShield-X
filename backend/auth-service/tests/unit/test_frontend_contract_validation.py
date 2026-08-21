"""Unit tests for Frontend DTO Contract Validation (Phase 3.9 Part 1C)."""

import pytest
from app.schemas.risk_aggregation_models import RiskCardDTO, RiskSummaryDTO


def test_frontend_contract_fields():
    card = RiskCardDTO(card_id="c1", category="CAT", score=10.0, risk_band="TRUSTED")
    summary = RiskSummaryDTO(title="Summary", risk_score=10.0, risk_band="TRUSTED")

    assert card.card_id == "c1"
    assert summary.risk_score == 10.0
