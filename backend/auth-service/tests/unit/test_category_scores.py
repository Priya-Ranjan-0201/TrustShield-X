"""Unit tests for Category Risk Scoring (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskCategoryScoreDTO


def test_category_score_dto():
    cs = RiskCategoryScoreDTO(
        category="NETWORK_THREAT",
        raw_score=15.0,
        normalized_score=15.0,
        risk_band="TRUSTED",
    )

    assert cs.category == "NETWORK_THREAT"
    assert cs.normalized_score == 15.0
