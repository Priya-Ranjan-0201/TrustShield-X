"""Unit tests for Confidence Fusion Service (Phase 3.9 Part 1A.25)."""

import pytest
from app.services.confidence_fusion_service import ConfidenceFusionService


def test_fuse_confidence_multi_high():
    service = ConfidenceFusionService()
    dto = service.fuse_confidence(
        finding_id="f1",
        evidence_confidences=["VERY_HIGH", "VERY_HIGH"],
    )

    assert dto.fused_confidence == "VERY_HIGH"
    assert dto.confidence_ceiling_applied is False
