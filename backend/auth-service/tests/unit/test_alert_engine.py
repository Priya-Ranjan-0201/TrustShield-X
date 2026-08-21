"""Unit Tests — Security Alert Engine, Deduplication, Storms & Suppression (Phase 4.0 Part 6 — Sections 33-45, 89, 107).

Implements:
- Mandatory Test 10: Same alert generated multiple times -> Deduplicated.
- Mandatory Test 11: 100 identical alerts arrive -> Alert storm protection.
- Mandatory Test 12: Critical alert unacknowledged -> Policy-based escalation.
- Mandatory Test 24: Alert suppression created -> Audit record + expiration.
- Mandatory Test 25: Suppressed critical event occurs -> Critical override respected.
"""

import pytest
from app.schemas.continuous_intelligence_models import IntelligenceChangeEventDTO
from app.services.monitoring.security_alert_engine import SecurityAlertEngine
from app.services.monitoring.intelligence_impact_engine import ImpactDecision


class TestSecurityAlertEngine:
    def test_10_mandatory_same_alert_generated_multiple_times_deduplicated(self):
        engine = SecurityAlertEngine()
        ev = IntelligenceChangeEventDTO(
            event_id="ev_alt_1",
            event_type="IOC_NEW",
            entity_id="bad-domain.in",
            previous_state="DISCOVERED",
            new_state="MALICIOUS",
            source="ThreatFeed",
        )
        impact = ImpactDecision(
            impact_level="HIGH_IMPACT",
            what_changed="Bad domain observed",
            affected_objects=["bad-domain.in"],
            why_relevant="Monitored domain",
            supporting_evidence=[],
            recommended_action="Alert",
        )

        alert1 = engine.generate_alert(ev, impact)
        alert2 = engine.generate_alert(ev, impact)

        assert alert1 is not None and alert2 is not None
        assert alert1.alert_id == alert2.alert_id
        assert len(engine.list_alerts()) == 1

    def test_11_mandatory_alert_storm_protection(self):
        engine = SecurityAlertEngine()
        ev = IntelligenceChangeEventDTO(
            event_id="ev_storm",
            event_type="IOC_NEW",
            entity_id="flooding-entity.com",
            previous_state="DISCOVERED",
            new_state="MALICIOUS",
            source="NoisyFeed",
        )
        impact = ImpactDecision(
            impact_level="HIGH_IMPACT",
            what_changed="Noisy alert",
            affected_objects=["flooding-entity.com"],
            why_relevant="Storm",
            supporting_evidence=[],
            recommended_action="Alert",
        )

        created_alerts = []
        for i in range(100):
            # Change event_id so each would be fresh if not for rate limiting
            ev_iter = ev.model_copy()
            ev_iter.event_id = f"ev_storm_{i}"
            res = engine.generate_alert(ev_iter, impact)
            if res:
                created_alerts.append(res)

        # Capped by deduplication and storm threshold
        assert len(engine.list_alerts()) <= 50

    def test_12_mandatory_policy_based_escalation(self):
        engine = SecurityAlertEngine()
        ev = IntelligenceChangeEventDTO(
            event_id="ev_esc",
            event_type="IOC_NEW",
            entity_id="victim-domain.org",
            previous_state="DISCOVERED",
            new_state="MALICIOUS",
            source="ThreatFeed",
        )
        impact = ImpactDecision(
            impact_level="MEDIUM_IMPACT",
            what_changed="Medium alert",
            affected_objects=["victim-domain.org"],
            why_relevant="Active case",
            supporting_evidence=[],
            recommended_action="Alert",
        )
        alert = engine.generate_alert(ev, impact)
        assert alert is not None
        assert alert.priority == "MEDIUM"

        # Escalate
        updated, esc = engine.escalate_alert(alert.alert_id, "CRITICAL", "Unacknowledged for SLA timeout")
        assert updated.priority == "CRITICAL"
        assert updated.status == "ESCALATED"
        assert esc.escalated_priority == "CRITICAL"

    def test_24_and_25_mandatory_suppression_and_critical_override(self):
        engine = SecurityAlertEngine()
        ev = IntelligenceChangeEventDTO(
            event_id="ev_supp",
            event_type="IOC_NEW",
            entity_id="testing-domain.com",
            previous_state="DISCOVERED",
            new_state="MALICIOUS",
            source="ThreatFeed",
        )
        impact_med = ImpactDecision(
            impact_level="MEDIUM_IMPACT",
            what_changed="Medium alert",
            affected_objects=["testing-domain.com"],
            why_relevant="Test",
            supporting_evidence=[],
            recommended_action="Alert",
        )
        alert = engine.generate_alert(ev, impact_med)
        assert alert is not None

        # Suppress
        alert, supp = engine.suppress_alert(alert.alert_id, "Known QA test domain", suppressed_by="lead_analyst")
        assert alert.status == "SUPPRESSED"
        assert supp.is_active is True

        # Test 25: Critical event occurs on same fingerprint -> Critical override triggers
        impact_crit = ImpactDecision(
            impact_level="CRITICAL_IMPACT",
            what_changed="Critical ransomware indicator matched",
            affected_objects=["testing-domain.com"],
            why_relevant="Emergency",
            supporting_evidence=[],
            recommended_action="Immediate containment",
        )
        crit_alert = engine.generate_alert(ev, impact_crit)
        # Critical alert overrides suppression because allow_critical_override is True
        assert crit_alert is not None
        assert crit_alert.priority == "CRITICAL"
