"""Unit tests for Composite Finding Split Operations (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import ConsolidationMetricsDTO


def test_consolidation_metrics_split_count():
    metrics = ConsolidationMetricsDTO(
        input_findings_count=2,
        split_findings_count=4,
    )

    assert metrics.split_findings_count == 4
