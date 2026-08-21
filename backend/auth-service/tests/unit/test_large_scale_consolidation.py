"""Unit tests for Large Scale Performance & Telemetry (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import ConsolidationMetricsDTO


def test_large_scale_metrics_dto():
    metrics = ConsolidationMetricsDTO(
        input_findings_count=10000,
        canonical_entities_count=4500,
        canonical_evidence_count=8200,
        duplicate_evidence_suppressed=1800,
        merged_findings_count=1200,
        split_findings_count=50,
        conflicted_findings_count=12,
    )

    assert metrics.input_findings_count == 10000
    assert metrics.duplicate_evidence_suppressed == 1800
