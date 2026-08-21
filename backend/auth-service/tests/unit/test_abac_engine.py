"""Unit Tests — ABAC Engine & Contextual Authorization (Phase 4.0 Part 8 — Sections 14-16, 93, 101).

Implements:
- Mandatory Test 5: User attempts access without MFA when MFA is required -> REQUIRE_MFA / AUTHENTICATION_FAILURE.
- Mandatory Test 10: Resource contains RESTRICTED classification -> classification clearance enforced.
"""

import pytest
from app.services.governance.abac_engine import ABACEngine


class TestABACEngineAndContextPolicy:
    def test_05_mandatory_mfa_required_by_policy_blocks_unverified_access(self):
        # Invariant (Test 5): User lacks MFA verification when required by policy -> Access blocked
        dec = ABACEngine.evaluate_abac(
            user_id="usr_01",
            user_roles=["SOC_ANALYST"],
            resource_id="inc_critical_01",
            resource_type="incident",
            mfa_verified=False,
            mfa_required_by_policy=True,
        )
        assert dec.allowed is False
        assert dec.decision == "REQUIRE_MFA"
        assert "multi-factor authentication" in dec.reason

        # Satisfied MFA -> Access allowed
        dec_mfa = ABACEngine.evaluate_abac(
            user_id="usr_01",
            user_roles=["SOC_ANALYST"],
            resource_id="inc_critical_01",
            resource_type="incident",
            mfa_verified=True,
            mfa_required_by_policy=True,
        )
        assert dec_mfa.allowed is True
        assert dec_mfa.decision == "ALLOW"

    def test_10_mandatory_data_classification_clearance_enforced(self):
        # Invariant (Test 10): Unprivileged user cannot access RESTRICTED or HIGHLY_RESTRICTED resources
        dec_unprivileged = ABACEngine.evaluate_abac(
            user_id="usr_viewer_01",
            user_roles=["REPORT_VIEWER"],
            resource_id="ev_forensic_dump_01",
            resource_type="evidence",
            classification="HIGHLY_RESTRICTED",
        )
        assert dec_unprivileged.allowed is False
        assert dec_unprivileged.decision == "DENY"
        assert "lacks clearance" in dec_unprivileged.reason

        # Privileged Security Admin -> Clearance verified
        dec_admin = ABACEngine.evaluate_abac(
            user_id="usr_sec_admin",
            user_roles=["SECURITY_ADMIN"],
            resource_id="ev_forensic_dump_01",
            resource_type="evidence",
            classification="HIGHLY_RESTRICTED",
        )
        assert dec_admin.allowed is True
        assert dec_admin.decision == "ALLOW"
