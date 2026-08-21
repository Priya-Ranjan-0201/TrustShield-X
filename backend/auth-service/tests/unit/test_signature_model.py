"""Unit Tests — Digital Signature Architecture (Phase 4.0 Part 3 — Section 84, Test 13)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService


class TestSignatureModel:
    """Mandatory Test Case 13: Unsigned report. Expected signature status: NOT_SIGNED. Never VERIFIED."""

    def test_unsigned_report_returns_not_signed(self):
        svc = ReportIntegrityService()
        sig = svc.generate_signature(artifact_id="art_unsigned", artifact_sha256="abc123hash", private_key=None)
        assert sig.status == "NOT_SIGNED"
        assert sig.signature == ""
        assert sig.status != "VERIFIED"
