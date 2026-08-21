"""Unit tests for Supporting Evidence Relationships (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import EvidenceRelationshipDTO


def test_supporting_evidence_dto():
    rel = EvidenceRelationshipDTO(
        source_evidence_id="ev_1",
        target_evidence_id="ev_2",
        relationship="CORROBORATES",
    )

    assert rel.relationship == "CORROBORATES"
