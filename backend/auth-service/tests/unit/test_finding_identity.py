"""Unit tests for Finding Identity Generation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_finding_identity_dto():
    finding = CanonicalFindingDTO(
        finding_id="finding_1",
        finding_type="NETWORK_ENDPOINT_OBSERVED",
        finding_category="NETWORK",
        title="Test Finding",
        description="Description",
    )

    assert finding.finding_id == "finding_1"
