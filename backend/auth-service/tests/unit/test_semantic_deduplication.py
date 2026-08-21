"""Unit tests for Semantic Deduplication (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_semantic_deduplication_finding():
    finding = CanonicalFindingDTO(
        finding_id="semantic_f1",
        finding_type="NETWORK_ENDPOINT_OBSERVED",
        finding_category="NETWORK",
        title="Static Endpoint",
        description="Description",
        source_count=2,
    )

    assert finding.source_count == 2
