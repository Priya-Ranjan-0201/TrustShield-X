"""Unit Tests — Report Integrity & Tampering Detection (Phase 4.0 Part 3 — Section 84, Test 12)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService


class TestReportIntegrity:
    """Mandatory Test Case 12: Corrupt stored artifact. Expected: Integrity verification fails."""

    def test_detect_corrupted_artifact(self):
        svc = ReportIntegrityService()
        original_bytes = b"Original Authentic Report Bytes"
        expected_sha = svc.calculate_artifact_hash(original_bytes)

        # Verify valid artifact passes
        valid_rec = svc.verify_artifact_integrity(
            artifact_bytes=original_bytes,
            expected_sha256=expected_sha,
            report_id="rep_test",
            artifact_id="art_test",
        )
        assert valid_rec.is_valid is True
        assert valid_rec.detected_tampering is False

        # Verify corrupted artifact fails
        corrupted_bytes = b"Corrupted Modified Report Bytes"
        corrupted_rec = svc.verify_artifact_integrity(
            artifact_bytes=corrupted_bytes,
            expected_sha256=expected_sha,
            report_id="rep_test",
            artifact_id="art_test",
        )
        assert corrupted_rec.is_valid is False
        assert corrupted_rec.detected_tampering is True
