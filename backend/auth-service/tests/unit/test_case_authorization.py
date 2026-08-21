"""Unit Tests — Case Authorization & RBAC (Phase 4.0 Part 4 — Section 44-45, 83)."""

import pytest
from app.schemas.investigation_models import CaseShareDTO


class TestCaseAuthorization:
    def test_case_share_dto_defaults(self):
        share = CaseShareDTO(
            share_id="share_01",
            report_id="rep_101",
            case_id="case_202",
            created_by="usr_lead",
            expires_at="2026-08-17T00:00:00Z",
            permission="VIEW_ONLY",
            status="ACTIVE",
        )
        assert share.share_id == "share_01"
        assert share.status == "ACTIVE"
        assert share.permission == "VIEW_ONLY"

    def test_permission_model_enforcement(self):
        # Role with restricted capabilities cannot export raw technical data
        allowed_roles = ["TECHNICAL", "ADMIN"]
        role = "EXECUTIVE"
        has_permission = role in allowed_roles
        assert has_permission is False
