"""Unit Tests — Case Sharing & Ephemeral Links (Phase 4.0 Part 4 — Sections 46-48, 83)."""

import pytest
from app.schemas.investigation_models import CaseShareDTO


class TestCaseSharing:
    def test_case_share_permissions(self):
        valid_perms = ["VIEW_ONLY", "DOWNLOAD_ALLOWED", "EVIDENCE_VIEW", "TECHNICAL_VIEW", "FULL_ACCESS"]
        share = CaseShareDTO(
            share_id="sh_01",
            report_id="rep_01",
            created_by="usr_01",
            expires_at="2026-08-17T00:00:00Z",
            permission="EVIDENCE_VIEW",
        )
        assert share.permission in valid_perms

    def test_case_share_lifecycle_status(self):
        valid_statuses = ["ACTIVE", "EXPIRED", "REVOKED"]
        share = CaseShareDTO(
            share_id="sh_02",
            report_id="rep_01",
            created_by="usr_01",
            expires_at="2026-08-17T00:00:00Z",
            status="REVOKED",
        )
        assert share.status in valid_statuses
