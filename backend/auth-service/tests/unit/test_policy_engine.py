"""Unit Tests — Governance Policy Engine, Simulation & Versioning (Phase 4.0 Part 8 — Sections 17-26, 95, 101).

Implements:
- Mandatory Test 6: Policy contains ALLOW and DENY conflict -> conflict detected.
- Mandatory Test 7: Published policy modified directly -> BLOCKED, new version required.
- Mandatory Test 16: Policy simulation executed -> zero production policy changes.
- Mandatory Test 17: Author attempts to approve own critical policy -> Separation of Duties violation.
"""

import pytest
from app.services.governance.policy_engine import PolicyEngine
from app.services.governance.policy_simulation_engine import PolicySimulationEngine


class TestPolicyEngineAndImmutability:
    def test_06_mandatory_policy_conflict_detection(self):
        engine = PolicyEngine()
        conflicting_rules = [
            {"resource": "report", "action": "export", "effect": "ALLOW"},
            {"resource": "report", "action": "export", "effect": "DENY", "reason": "No exports on weekends"},
        ]

        # Invariant (Test 6): Direct ALLOW + DENY collision is detected
        conflicts = engine.detect_conflicts(conflicting_rules)
        assert len(conflicts) > 0
        assert any("Direct collision" in c for c in conflicts)

    def test_07_mandatory_published_policy_direct_mutation_blocked(self):
        engine = PolicyEngine()
        pol, ver = engine.publish_policy(
            policy_id="pol_export_restriction",
            organization_id="org_1",
            name="Export Policy",
            policy_type="EXPORT",
            rules=[{"resource": "report", "action": "export", "effect": "REQUIRE_APPROVAL"}],
            created_by="admin_alice@trustshield.internal",
            approved_by="lead_bob@trustshield.internal",
        )
        assert ver.version_number == 1

        # Invariant (Test 7): Direct modification of published policy raises PermissionError
        with pytest.raises(PermissionError):
            engine.direct_modify_blocked("pol_export_restriction")

    def test_16_mandatory_policy_simulation_zero_production_mutation(self):
        engine = PolicyEngine()
        pol, _ = engine.publish_policy(
            policy_id="pol_sim_test",
            organization_id="org_1",
            name="Simulation Test Policy",
            policy_type="ACCESS_CONTROL",
            rules=[{"resource": "incident", "action": "delete", "effect": "DENY"}],
            created_by="admin@trustshield.internal",
            approved_by="lead@trustshield.internal",
        )

        initial_count = len(engine.list_policies())
        sim = PolicySimulationEngine.simulate_policy(pol)

        # Invariant (Test 16): Zero mutations to production policies
        assert sim.simulation_verdict == "SIMULATION_PASSED_ZERO_PRODUCTION_MUTATION"
        assert sim.new_denials_count == 1
        assert len(engine.list_policies()) == initial_count

    def test_17_mandatory_requester_cannot_approve_own_policy(self):
        engine = PolicyEngine()

        # Invariant (Test 17): Author cannot self-approve policy
        with pytest.raises(PermissionError):
            engine.publish_policy(
                policy_id="pol_sod_test",
                organization_id="org_1",
                name="SoD Test Policy",
                policy_type="ACCESS_CONTROL",
                rules=[],
                created_by="admin_alice@trustshield.internal",
                approved_by="admin_alice@trustshield.internal",
                enforce_separation_of_duties=True,
            )
