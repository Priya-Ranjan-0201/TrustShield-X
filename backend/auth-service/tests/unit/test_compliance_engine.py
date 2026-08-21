"""Unit Tests — Compliance Control Mapping & Governance Posture (Phase 4.0 Part 8 — Sections 53-63, 99, 101)."""

import pytest
from app.services.governance.compliance_engine import ComplianceEngine
from app.services.governance.governance_posture_engine import GovernancePostureEngine


class TestComplianceEngineAndPosture:
    def test_framework_registration_and_assessment(self):
        comp = ComplianceEngine()

        fws = comp.list_frameworks()
        fw_ids = [f.framework_id for f in fws]
        assert "iso_27001" in fw_ids
        assert "soc_2" in fw_ids
        assert "dpdp_2023" in fw_ids

        # Assess ISO 27001
        ass = comp.assess_framework("iso_27001", "org_1")
        assert ass.score_percentage > 0.0
        assert ass.implemented_count > 0

    def test_compliance_report_contains_non_certification_disclaimer(self):
        comp = ComplianceEngine()

        rep = comp.generate_compliance_report("soc_2", "org_1")
        assert rep.score_percentage > 0.0
        # Invariant: Must not claim formal third-party certification
        assert "does not constitute formal third-party certification" in rep.executive_summary

    def test_evidence_linking_to_controls(self):
        comp = ComplianceEngine()

        ev = comp.link_evidence(
            control_id="CC6.1",
            resource_type="audit_log",
            resource_id="aud_101",
            source="TruthShield Audit Engine",
            integrity_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )
        assert ev.status == "VERIFIED"
        assert len(ev.integrity_hash) == 64

    def test_governance_posture_score_calculation(self):
        posture = GovernancePostureEngine.evaluate_posture(
            organization_id="org_1",
            active_users_count=10,
            mfa_enabled_users_count=10,
            active_policies_count=5,
            implemented_controls_count=10,
            total_controls_count=10,
            audit_integrity_verified=True,
        )
        assert posture.overall_posture_score >= 90.0
        assert posture.mfa_coverage == 100.0
        assert posture.audit_coverage == 100.0
