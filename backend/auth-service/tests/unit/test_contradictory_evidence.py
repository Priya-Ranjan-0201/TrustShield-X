"""Unit tests for Contradictory Evidence & Conflict Handling (Phase 3.9 Part 1A.22)."""

import pytest
from app.schemas.behavioral_correlation_models import BehaviorConflictDTO


def test_contradictory_evidence_dto():
    conflict = BehaviorConflictDTO(
        conflict_id="conf_1",
        conflict_type="CONTRADICTORY_CONFIGURATION",
        evidence_a="Manifest: cleartextTrafficPermitted=false",
        evidence_b="Code: http:// Endpoint",
        resolution_status="CONFLICTED",
    )

    assert conflict.conflict_type == "CONTRADICTORY_CONFIGURATION"
    assert conflict.resolution_status == "CONFLICTED"
