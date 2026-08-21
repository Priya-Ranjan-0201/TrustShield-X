"""Unit tests for Confidence Ceiling Enforcement (Phase 3.9 Part 1A.25)."""

import pytest
from app.services.confidence_fusion_service import ConfidenceFusionService


def test_confidence_ceiling_reflection():
    service = ConfidenceFusionService()
    dto = service.fuse_confidence(
        finding_id="f1",
        evidence_confidences=["VERY_HIGH"],
        has_unresolved_reflection=True,
    )

    assert dto.fused_confidence == "MEDIUM"
    assert dto.confidence_ceiling_applied is True
    assert "Reflection" in dto.ceiling_reason
