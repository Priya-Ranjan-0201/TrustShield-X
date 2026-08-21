"""Unit Tests — RBAC Engine & Least Privilege Governance (Phase 4.0 Part 8 — Sections 8-13, 92, 101).

Implements:
- Mandatory Test 3: Read-only user attempts response execution -> ACCESS_DENIED.
- Mandatory Test 4: Auditor attempts destructive action -> ACCESS_DENIED.
"""

import pytest
from app.services.governance.rbac_engine import RBACEngine


class TestRBACEngineAndLeastPrivilege:
    def test_03_mandatory_read_only_user_cannot_execute_response(self):
        engine = RBACEngine()

        # Invariant (Test 3): READ_ONLY_USER must be denied response execution
        dec = engine.evaluate_rbac_access(
            user_id="usr_reader_01",
            user_roles=["READ_ONLY_USER"],
            resource="response",
            action="execute",
        )
        assert dec.allowed is False
        assert dec.decision == "DENY"
        assert "lacks required permission" in dec.reason

    def test_04_mandatory_auditor_cannot_perform_destructive_actions(self):
        engine = RBACEngine()

        # Invariant (Test 4): AUDITOR role must be denied destructive deletion/execution
        dec_delete = engine.evaluate_rbac_access(
            user_id="usr_auditor_01",
            user_roles=["AUDITOR"],
            resource="incident",
            action="delete",
        )
        assert dec_delete.allowed is False
        assert dec_delete.decision == "DENY"

        dec_exec = engine.evaluate_rbac_access(
            user_id="usr_auditor_01",
            user_roles=["AUDITOR"],
            resource="response",
            action="execute",
        )
        assert dec_exec.allowed is False
        assert dec_exec.decision == "DENY"

    def test_soc_analyst_permissions(self):
        engine = RBACEngine()

        dec_read = engine.evaluate_rbac_access(
            user_id="usr_soc_01",
            user_roles=["SOC_ANALYST"],
            resource="incident",
            action="read",
        )
        assert dec_read.allowed is True
        assert dec_read.decision == "ALLOW"

        # SOC Analyst cannot execute high impact action directly without senior/responder role
        dec_exec = engine.evaluate_rbac_access(
            user_id="usr_soc_01",
            user_roles=["SOC_ANALYST"],
            resource="response",
            action="execute",
        )
        assert dec_exec.allowed is False

    def test_role_creation_and_version_immutability(self):
        engine = RBACEngine()

        role, ver1 = engine.create_or_update_role(
            name="Tier 1 Triager",
            permissions=["incident:read", "alert:acknowledge"],
        )
        assert role.version == 1
        assert ver1.version_number == 1
        assert len(ver1.content_hash) == 64

        # Update role permissions -> version 2
        role2, ver2 = engine.create_or_update_role(
            name="Tier 1 Triager",
            permissions=["incident:read", "alert:acknowledge", "evidence:read"],
        )
        assert role2.version == 2
        assert ver2.version_number == 2
