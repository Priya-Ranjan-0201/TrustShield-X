"""Unit tests for Composite Risk Interactions (Phase 3.9 Part 1B)."""

import pytest
from app.schemas.risk_aggregation_models import RiskInteractionDTO


def test_risk_interaction_dto():
    intr = RiskInteractionDTO(
        interaction_id="intr_1",
        factor_a_id="f1",
        factor_b_id="f2",
        amplification_bonus=5.0,
        description="SMS Permission + Dataflow -> Network Sink",
    )

    assert intr.amplification_bonus == 5.0
