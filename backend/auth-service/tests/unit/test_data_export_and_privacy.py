"""Unit Tests — Data Export Governance & Privacy Workflows (Phase 4.0 Part 8 — Sections 40-44, 97, 101).

Implements:
- Mandatory Test 9: Unauthorized export -> ACCESS_DENIED.
- Mandatory Test 10: Export contains RESTRICTED resource -> classification policy enforced.
"""

import pytest
from app.services.governance.data_export_engine import DataExportEngine
from app.services.governance.privacy_request_engine import PrivacyRequestEngine
from app.services.governance.legal_hold_engine import LegalHoldEngine


class TestDataExportAndPrivacyGovernance:
    def test_09_mandatory_unauthorized_export_denied(self):
        engine = DataExportEngine()

        # Invariant (Test 9): Non-privileged user (READ_ONLY_USER) cannot create export
        with pytest.raises(PermissionError) as exc_info:
            engine.create_data_export(
                organization_id="org_1",
                requester_id="usr_reader_01",
                requester_roles=["READ_ONLY_USER"],
                scope="CASE",
                resource_data=[{"report_id": "rep_101"}],
            )
        assert "lacks authorization" in str(exc_info.value)

    def test_10_mandatory_restricted_export_enforces_classification_clearance(self):
        engine = DataExportEngine()

        # Senior analyst has export perm for normal data, but lacks clearance for HIGHLY_RESTRICTED credentials
        with pytest.raises(PermissionError) as exc_info:
            engine.create_data_export(
                organization_id="org_1",
                requester_id="usr_analyst_01",
                requester_roles=["SENIOR_ANALYST"],
                scope="CREDENTIALS",
                resource_data=[{"vault_item": "api_secret"}],
                classification="HIGHLY_RESTRICTED",
            )
        assert "lacks security clearance" in str(exc_info.value)

        # Security Admin has sufficient clearance
        manifest = engine.create_data_export(
            organization_id="org_1",
            requester_id="usr_sec_admin",
            requester_roles=["SECURITY_ADMIN"],
            scope="CREDENTIALS",
            resource_data=[{"vault_item": "api_secret"}],
            classification="HIGHLY_RESTRICTED",
        )
        assert manifest.status == "READY"
        assert len(manifest.integrity_hash) == 64
        assert manifest.download_token.startswith("dlt_")

    def test_dpdp_privacy_request_with_legal_hold(self):
        lh_engine = LegalHoldEngine()
        priv_engine = PrivacyRequestEngine(legal_hold_engine=lh_engine)

        # Principal is on legal hold
        lh_engine.apply_legal_hold("org_1", "data_principal", "user_subject_01", "Subpoena", "legal@corp.in")

        req = priv_engine.submit_privacy_request("org_1", "user_subject_01", "DELETION", "Right to Erasure")
        processed = priv_engine.process_privacy_request(req.request_id, "dpo@corp.in", verify_identity=True)

        # Invariant: Deletion is REJECTED due to legal hold
        assert processed.status == "REJECTED"
        assert "legal hold" in processed.reason
