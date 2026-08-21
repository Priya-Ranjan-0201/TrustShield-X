"""Unit tests for Evidence Consolidation Frontend Contract DTOs (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import EvidenceCardDTO, EvidenceSummaryDTO


def test_frontend_contract_dtos():
    card = EvidenceCardDTO(
        card_id="card_1",
        title="Observed Static Network Endpoint",
        finding_id="f1",
        status="CORRELATED",
        confidence="HIGH",
    )
    summary = EvidenceSummaryDTO(
        title="Summary Title",
        summary_text="Text",
        consolidated_findings_count=5,
    )

    assert card.title == "Observed Static Network Endpoint"
    assert summary.consolidated_findings_count == 5
