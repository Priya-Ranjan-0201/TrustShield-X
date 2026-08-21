"""Unit tests for Report Frontend Contract (Phase 4.0 Part 1)."""

import pytest
from app.schemas.digital_trust_report_models import TrustOverviewDTO


def test_report_frontend_contract_overview():
    overview = TrustOverviewDTO(
        risk_score=25.0,
        risk_band="LOW_RISK",
        confidence="HIGH",
        evidence_sufficiency="SUFFICIENT",
    )

    assert overview.risk_score == 25.0
    assert overview.risk_band == "LOW_RISK"
