"""Unit Tests — Session Governance, API Key Hashing & Service Accounts (Phase 4.0 Part 8 — Sections 72-79, 100, 101).

Implements:
- Mandatory Test 11: Revoked API key reused -> ACCESS_DENIED.
- Mandatory Test 12: Raw API key requested after creation -> NOT returned.
- Mandatory Test 19: Service account requesting unauthorized resource -> ACCESS_DENIED.
"""

import pytest
from app.services.governance.api_key_service import APIKeyService
from app.services.governance.session_governance_service import SessionGovernanceService
from app.services.governance.rbac_engine import RBACEngine


class TestAPIKeyAndSessionGovernance:
    def test_11_mandatory_revoked_api_key_reuse_denied(self):
        svc = APIKeyService()

        # Create API key
        resp, meta = svc.create_api_key(
            organization_id="org_1",
            name="SIEM Ingestion Key",
            owner_id="admin@corp.in",
            permissions=["alert:read", "alert:create"],
        )
        raw_key = resp.raw_key

        # Key verifies when active
        verified_meta = svc.verify_api_key(raw_key)
        assert verified_meta is not None
        assert verified_meta.status == "ACTIVE"

        # Revoke key
        svc.revoke_api_key(resp.key_id)

        # Invariant (Test 11): Verification of revoked key fails (returns None)
        assert svc.verify_api_key(raw_key) is None

    def test_12_mandatory_raw_api_key_never_stored_or_reexposed(self):
        svc = APIKeyService()

        # Create API key
        resp, meta = svc.create_api_key(
            organization_id="org_1",
            name="Production Ingestion Agent",
            owner_id="admin@corp.in",
            permissions=["incident:read"],
        )

        # Raw key is ONLY in resp
        assert resp.raw_key.startswith("tsx_")

        # Stored metadata does NOT contain raw key
        stored_keys = svc.list_api_keys("org_1")
        target_meta = next(k for k in stored_keys if k.key_id == resp.key_id)

        # Invariant (Test 12): No raw_key attribute in stored metadata; only hashed_secret exists
        assert not hasattr(target_meta, "raw_key")
        assert target_meta.hashed_secret != resp.raw_key
        assert len(target_meta.hashed_secret) == 64

    def test_19_mandatory_service_account_unauthorized_action_denied(self):
        svc = APIKeyService()
        rbac = RBACEngine()

        # Service account provisioned ONLY for read
        sa = svc.create_service_account(
            organization_id="org_1",
            name="Metric Exporter SA",
            permissions=["metrics:read", "health:read"],
            created_by="admin@corp.in",
        )

        # Custom role for SA
        role, _ = rbac.create_or_update_role(
            name=f"SA_ROLE_{sa.service_account_id}",
            permissions=sa.permissions,
        )

        # Invariant (Test 19): Service account requesting write/execute is DENIED
        dec = rbac.evaluate_rbac_access(
            user_id=sa.service_account_id,
            user_roles=[role.name],
            resource="incident",
            action="delete",
        )
        assert dec.allowed is False
        assert dec.decision == "DENY"

    def test_session_lifecycle_and_revocation(self):
        session_svc = SessionGovernanceService()

        sess = session_svc.create_session("usr_1", "org_1", mfa_verified=True)
        assert sess.status == "ACTIVE"

        session_svc.revoke_session(sess.session_id)
        assert session_svc.get_session(sess.session_id).status == "REVOKED"
