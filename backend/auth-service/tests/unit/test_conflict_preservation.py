"""Unit tests for Contradiction Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_conflicted_status_preserves_count():
    finding = CanonicalFindingDTO(
        finding_id="f_conflicted",
        finding_type="STORAGE_CONFIGURATION",
        finding_category="STORAGE",
        title="Conflicted Storage Claims",
        description="Description",
        status="CONFLICTED",
        contradiction_count=1,
    )

    assert finding.status == "CONFLICTED"
    assert finding.contradiction_count == 1
