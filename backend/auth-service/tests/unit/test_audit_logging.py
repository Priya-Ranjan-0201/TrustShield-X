"""Unit Tests — Report Audit Logging (Phase 4.0 Part 3 — Section 81)."""

import pytest
from app.schemas.report_rendering_models import ReportDownloadAuditDTO


class TestAuditLogging:
    """Section 81: Track download audits, verifications, and generation events."""

    def test_download_audit_dto(self):
        audit = ReportDownloadAuditDTO(
            audit_id="aud_123",
            artifact_id="art_123",
            user_id="user_admin",
            ip_address="192.168.1.10",
            downloaded_at="2026-08-14T00:00:00Z",
        )
        assert audit.audit_id == "aud_123"
        assert audit.user_id == "user_admin"
        assert audit.ip_address == "192.168.1.10"
