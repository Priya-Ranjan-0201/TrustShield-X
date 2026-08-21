"""Unit tests for Compatible Finding Merge Operations (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import ConsolidationMetricsDTO


def test_consolidation_metrics_merged_count():
    metrics = ConsolidationMetricsDTO(
        input_findings_count=10,
        canonical_entities_count=5,
        canonical_evidence_count=8,
        merged_findings_count=3,
    )

    assert metrics.merged_findings_count == 3
