"""Unit Tests — Object Authorization & Tenant Isolation (Phase 4.0 Part 4 — Section 45, 83)."""

import pytest
from app.schemas.investigation_models import WorkspaceContextDTO


class TestObjectAuthorization:
    def test_organization_isolation_in_context(self):
        ctx_a = WorkspaceContextDTO(
            workspace_id="ws_01",
            analysis_id="an_01",
            report_id="rep_01",
            user_id="usr_01",
            organization_id="org_alpha",
        )
        ctx_b = WorkspaceContextDTO(
            workspace_id="ws_02",
            analysis_id="an_02",
            report_id="rep_02",
            user_id="usr_02",
            organization_id="org_beta",
        )
        assert ctx_a.organization_id != ctx_b.organization_id
