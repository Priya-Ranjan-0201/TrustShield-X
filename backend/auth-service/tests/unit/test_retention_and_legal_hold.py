"""Unit Tests — Data Retention, Legal Hold & Deletion Governance (Phase 4.0 Part 8 — Sections 31-39, 96, 101).

Implements:
- Mandatory Test 8: Retention job encounters legal hold -> deletion blocked.
- Mandatory Test 15: User requests deletion of evidence under legal hold -> BLOCKED.
"""

import pytest
from datetime import datetime, timezone, timedelta
from app.services.governance.legal_hold_engine import LegalHoldEngine
from app.services.governance.data_retention_engine import DataRetentionEngine
from app.services.governance.data_deletion_engine import DataDeletionEngine


class TestDataRetentionAndLegalHoldShields:
    def test_08_mandatory_retention_job_encounters_legal_hold_deletion_blocked(self):
        lh_engine = LegalHoldEngine()
        ret_engine = DataRetentionEngine(legal_hold_engine=lh_engine)

        # Apply Legal Hold to an old incident evidence record
        lh_engine.apply_legal_hold(
            organization_id="org_1",
            resource_type="evidence",
            resource_id="ev_court_subpoena_01",
            reason="Court Subpoena 2026-CV-99",
            created_by="legal_counsel@corp.in",
        )

        # Resource created 2 years ago (exceeds 365 days default retention)
        two_years_ago = datetime.now(timezone.utc) - timedelta(days=730)

        # Invariant (Test 8): Retention state must evaluate to LEGAL_HOLD, shielding from deletion
        state = ret_engine.evaluate_resource_retention_state(
            organization_id="org_1",
            resource_type="evidence",
            resource_id="ev_court_subpoena_01",
            created_at=two_years_ago,
        )
        assert state == "LEGAL_HOLD"

    def test_15_mandatory_user_deletion_request_on_legal_hold_blocked(self):
        lh_engine = LegalHoldEngine()
        del_engine = DataDeletionEngine(legal_hold_engine=lh_engine)

        # Resource is under active legal hold
        lh_engine.apply_legal_hold(
            organization_id="org_1",
            resource_type="evidence",
            resource_id="ev_critical_forensic_01",
            reason="Regulatory audit active",
            created_by="compliance@corp.in",
        )

        # Invariant (Test 15): Deletion request MUST raise PermissionError and be BLOCKED
        with pytest.raises(PermissionError) as exc_info:
            del_engine.process_deletion_request(
                organization_id="org_1",
                resource_type="evidence",
                resource_id="ev_critical_forensic_01",
                requested_by="analyst@corp.in",
            )
        assert "protected by active legal hold" in str(exc_info.value)
