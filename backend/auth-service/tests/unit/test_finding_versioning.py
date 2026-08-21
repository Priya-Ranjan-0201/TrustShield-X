"""Unit tests for Finding Engine Versioning (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import FindingVersionDTO


def test_finding_version_dto():
    ver = FindingVersionDTO(
        finding_id="f1",
        finding_version="1.0.0",
        engine_version="1.0.0",
    )

    assert ver.finding_version == "1.0.0"
