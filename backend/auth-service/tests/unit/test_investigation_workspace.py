"""Unit Tests — Investigation Workspace (Phase 4.0 Part 4 — Section 83)."""

import pytest
from app.schemas.investigation_models import (
    InvestigationWorkspaceDTO,
    WorkspaceContextDTO,
    WorkspaceStateDTO,
)
from app.services.investigation_orchestrator import InvestigationOrchestrator


class TestInvestigationWorkspace:
    def test_workspace_context_creation(self):
        ctx = WorkspaceContextDTO(
            workspace_id="ws_101",
            case_id="case_202",
            analysis_id="an_303",
            report_id="rep_404",
            user_id="usr_01",
            organization_id="org_sec",
            role="ANALYST",
        )
        assert ctx.workspace_id == "ws_101"
        assert ctx.role == "ANALYST"
        assert ctx.organization_id == "org_sec"

    def test_workspace_dto(self):
        ctx = WorkspaceContextDTO(
            workspace_id="ws_101",
            analysis_id="an_303",
            report_id="rep_404",
            user_id="usr_01",
        )
        ws = InvestigationWorkspaceDTO(
            workspace_id="ws_101",
            title="Active Phishing Investigation",
            context=ctx,
            status="ACTIVE",
        )
        assert ws.workspace_id == "ws_101"
        assert ws.status == "ACTIVE"

    def test_role_aware_views(self):
        orch = InvestigationOrchestrator()
        exec_view = orch.get_role_view_config("EXECUTIVE")
        assert exec_view.role == "EXECUTIVE"
        assert exec_view.show_raw_technical_data is False

        tech_view = orch.get_role_view_config("TECHNICAL")
        assert tech_view.role == "TECHNICAL"
        assert tech_view.show_raw_technical_data is True

        auditor_view = orch.get_role_view_config("AUDITOR")
        assert auditor_view.role == "AUDITOR"
        assert auditor_view.show_audit_metadata is True
