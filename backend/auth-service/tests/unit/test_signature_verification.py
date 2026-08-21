"""Unit Tests — Signature Verification (Phase 4.0 Part 3 — Section 84, Test 14)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService


class TestSignatureVerification:
    """Mandatory Test Case 14: Signed report with invalid signature/tampered bytes. Expected: Verification failure."""

    def test_signed_artifact_valid_verification(self):
        svc = ReportIntegrityService()
        data = b"Authentic Signed Bytes"
        h = svc.calculate_artifact_hash(data)
        sig = svc.generate_signature(artifact_id="art_sig", artifact_sha256=h, private_key="test-key-123")
        assert sig.status == "SIGNED"
        assert svc.verify_signature(sig, data) is True

    def test_tampered_artifact_fails_signature_verification(self):
        svc = ReportIntegrityService()
        data = b"Authentic Signed Bytes"
        h = svc.calculate_artifact_hash(data)
        sig = svc.generate_signature(artifact_id="art_sig", artifact_sha256=h, private_key="test-key-123")

        tampered = b"Modified Bytes"
        assert svc.verify_signature(sig, tampered) is False
