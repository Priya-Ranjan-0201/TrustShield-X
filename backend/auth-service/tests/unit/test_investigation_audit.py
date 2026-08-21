"""Unit Tests — Investigation Audit Logging (Phase 4.0 Part 4 — Sections 49, 81, 83)."""

import pytest
from app.schemas.investigation_models import InvestigationAuditEventDTO


class TestInvestigationAudit:
    def test_investigation_audit_event_dto(self):
        evt = InvestigationAuditEventDTO(
            event_id="aud_01",
            user_id="usr_analyst",
            case_id="case_01",
            analysis_id="an_01",
            action="evidence_viewed",
            object_type="EVIDENCE",
            object_id="EV_01",
            timestamp="2026-08-14T10:00:00Z",
        )
        assert evt.event_id == "aud_01"
        assert evt.action == "evidence_viewed"
        assert evt.object_type == "EVIDENCE"
