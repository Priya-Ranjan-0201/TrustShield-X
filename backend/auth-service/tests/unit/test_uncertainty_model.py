"""Unit tests for Uncertainty Model (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorFindingDTO


def test_uncertainty_model_dto():
    f = BehaviorFindingDTO(
        finding_id="f_uncert",
        finding_type="INFERRED_BEHAVIOR",
        category="REMOTE_CONFIGURATION",
        evidence_strength="WEAK",
        confidence="LOW",
        resolution_status="INFERRED",
        summary="Inferred potential behavior",
    )

    assert f.resolution_status == "INFERRED"
    assert f.confidence == "LOW"
