"""Unit tests for Finding Lineage Tracking (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import FindingLineageDTO


def test_finding_lineage_dto():
    lin = FindingLineageDTO(
        lineage_id="lin_1",
        finding_id="f1",
        parent_evidence_id="ev1",
        transformation_step="EVIDENCE_CONSOLIDATION",
    )

    assert lin.lineage_id == "lin_1"
    assert lin.parent_evidence_id == "ev1"
