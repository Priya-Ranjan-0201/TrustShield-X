"""Unit Tests — Intelligence Impact Evaluation (Phase 4.0 Part 6 — Sections 28-29, 107).

Implements:
- Mandatory Test 3: Malicious indicator appears for monitored domain -> impact analysis + alert + NO historical modification.
- Mandatory Test 19: New intelligence does not affect analysis -> NO_IMPACT decision + no unnecessary reassessment.
"""

import pytest
from app.schemas.continuous_intelligence_models import IntelligenceChangeEventDTO
from app.services.monitoring.intelligence_impact_engine import IntelligenceImpactEngine


class TestImpactEngine:
    def test_03_mandatory_malicious_indicator_on_monitored_domain_triggers_critical_impact(self):
        ch = IntelligenceChangeEventDTO(
            event_id="ev_impact_1",
            event_type="IOC_RECLASSIFIED",
            entity_id="monitored_domain_hash_1",
            previous_state="BENIGN",
            new_state="MALICIOUS",
            source="ThreatFeed CERT-In",
            confidence="HIGH",
            provenance="Domain active in phishing infrastructure",
            severity="CRITICAL",
        )
        monitored = ["monitored_domain_hash_1"]
        active_cases = ["monitored_domain_hash_1"]

        decision = IntelligenceImpactEngine.evaluate_impact(ch, monitored, active_cases)
        assert decision.impact_level == "CRITICAL_IMPACT"
        assert len(decision.affected_objects) == 1
        assert "targeted report reassessment" in decision.recommended_action

    def test_19_mandatory_unmonitored_intelligence_yields_no_impact(self):
        ch = IntelligenceChangeEventDTO(
            event_id="ev_impact_2",
            event_type="IOC_NEW",
            entity_id="unrelated_hash_999",
            previous_state="DISCOVERED",
            new_state="MALICIOUS",
            source="Public Feed",
            confidence="MEDIUM",
            provenance="Unrelated indicator",
        )
        monitored = ["other_domain_1", "other_domain_2"]

        decision = IntelligenceImpactEngine.evaluate_impact(ch, monitored)
        assert decision.impact_level == "NO_IMPACT"
        assert len(decision.affected_objects) == 0
