"""Unit Tests — Audit Immutability, Hash Chaining & Sanitization (Phase 4.0 Part 8 — Sections 45-52, 98, 101).

Implements:
- Mandatory Test 13: Audit event modified -> integrity failure detected.
- Mandatory Test 14: Admin attempts to delete audit event -> BLOCKED.
- Mandatory Test 20: Sensitive credentials in audit metadata -> sanitized and redacted.
"""

import pytest
from app.services.governance.audit_service import AuditService
from app.services.governance.audit_intelligence_engine import AuditIntelligenceEngine


class TestAuditServiceAndImmutability:
    def test_13_mandatory_audit_tamper_detection_via_hash_chain(self):
        audit = AuditService()

        # Record events
        e1 = audit.record_event("org_1", "usr_1", "login", "auth", "session_1")
        e2 = audit.record_event("org_1", "usr_1", "policy_change", "policy", "pol_1")
        e3 = audit.record_event("org_1", "usr_1", "response_execute", "action", "act_1")

        # 1. Unmodified chain verifies
        assert audit.verify_integrity() is True

        # 2. Tamper with e2
        e2.reason = "Altered unauthorized reason"

        # Invariant (Test 13): Hash chain validation MUST fail
        assert audit.verify_integrity() is False

    def test_14_mandatory_audit_deletion_is_blocked(self):
        audit = AuditService()
        e1 = audit.record_event("org_1", "usr_admin", "user_create", "user", "usr_new")

        # Invariant (Test 14): Audit deletion attempt raises PermissionError and is BLOCKED
        with pytest.raises(PermissionError) as exc_info:
            audit.delete_event_blocked(e1.audit_id)
        assert "cannot be deleted" in str(exc_info.value)

    def test_20_mandatory_sensitive_data_redacted_from_audit(self):
        audit = AuditService()

        # Input metadata containing raw password and bearer tokens
        raw_meta = {
            "user_email": "target@corp.in",
            "password": "SuperSecretPassword123!",
            "api_key": "raw_secret_key_value",
            "auth_header": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.dummy",
        }

        event = audit.record_event(
            organization_id="org_1",
            actor_id="usr_1",
            action="login_attempt",
            resource_type="auth",
            resource_id="session_01",
            reason="Login with password=SuperSecretPassword123!",
            metadata=raw_meta,
        )

        # Invariant (Test 20): Raw secret values MUST NOT appear in audit records
        assert event.metadata["password"] == "[REDACTED]"
        assert event.metadata["api_key"] == "[REDACTED]"
        assert "SuperSecretPassword123!" not in event.reason

    def test_audit_intelligence_detects_excessive_denials_and_mass_exports(self):
        audit = AuditService()
        events = []
        for i in range(4):
            events.append(audit.record_event("org_1", "usr_attacker", "export", "report", f"rep_{i}", result="SUCCESS"))
            events.append(audit.record_event("org_1", "usr_attacker", "delete", "policy", f"pol_{i}", result="DENIED"))

        alerts = AuditIntelligenceEngine.analyze_audit_stream(events)
        assert len(alerts) >= 2
        types = [a.alert_type for a in alerts]
        assert "MASS_EXPORT" in types
        assert "EXCESSIVE_DENIALS" in types
