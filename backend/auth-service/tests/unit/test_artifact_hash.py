"""Unit Tests — Artifact Hash & SHA-256 (Phase 4.0 Part 3 — Section 38)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService


class TestArtifactHash:
    """Section 38: Verify SHA-256 artifact hashing."""

    def test_artifact_hash_calculation(self):
        svc = ReportIntegrityService()
        data1 = b"Hello Report Data 1"
        data2 = b"Hello Report Data 2"
        h1 = svc.calculate_artifact_hash(data1)
        h2 = svc.calculate_artifact_hash(data2)
        assert len(h1) == 64
        assert len(h2) == 64
        assert h1 != h2

    def test_empty_artifact_hash(self):
        svc = ReportIntegrityService()
        h_empty = svc.calculate_artifact_hash(b"")
        assert h_empty == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
