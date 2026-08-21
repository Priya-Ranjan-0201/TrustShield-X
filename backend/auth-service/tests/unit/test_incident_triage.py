"""Unit Tests — Incident Triage & Safety Engine (Phase 4.0 Part 7 — Sections 17-19, 90, 92).

Implements:
- Mandatory Test 1: AI recommends blocking domain -> Recommendation ONLY, NO automatic execution.
- Mandatory Test 21: High-confidence malware alert -> high-priority triage.
- Mandatory Test 22: Low-confidence audio alert -> uncertainty preserved.
- Mandatory Test 23: Conflicting threat intelligence -> CONFLICTED evidence state.
- Mandatory Test 24: Missing evidence -> triage explicitly identifies uncertainty.
"""

import pytest
from app.schemas.soc_operations_models import SecurityIncidentDTO, SOCAlertDTO
from app.services.soc.incident_triage_engine import IncidentTriageEngine


class TestIncidentTriageAndSafety:
    def test_01_mandatory_ai_recommends_action_recommendation_only_no_execution(self):
        incident = SecurityIncidentDTO(
            incident_id="inc_phish_1",
            title="Phishing Threat",
            incident_type="PHISHING_INCIDENT",
            severity="HIGH",
        )
        alert = SOCAlertDTO(
            alert_id="alt_p1",
            title="Credential Phishing Domain",
            category="PHISHING",
            entity_ids=["steal-bank-creds.in"],
        )

        triage = IncidentTriageEngine.triage_incident(incident, [alert])

        # Recommended actions are proposed
        assert len(triage.recommended_actions) > 0
        block_action = next((a for a in triage.recommended_actions if a["action_type"] == "BLOCK_DOMAIN"), None)
        assert block_action is not None
        # Mandatory Safety Invariant: Action requires approval and is NOT executed automatically
        assert block_action["requires_approval"] is True
        assert block_action["target"] == "steal-bank-creds.in"

    def test_21_mandatory_high_confidence_malware_alert_triage(self):
        incident = SecurityIncidentDTO(
            incident_id="inc_mal_1",
            title="Ransomware APK Dropper",
            incident_type="MALWARE_INCIDENT",
            severity="CRITICAL",
            priority="CRITICAL",
            confidence="HIGH",
        )
        alert = SOCAlertDTO(
            alert_id="alt_m1",
            title="Ransomware Signature Detected",
            category="MALWARE",
            severity="CRITICAL",
            confidence="HIGH",
            evidence_ids=["ev_sig_match_1"],
        )
        triage = IncidentTriageEngine.triage_incident(incident, [alert])
        assert triage.classification == "MALWARE_INCIDENT"
        assert triage.severity == "CRITICAL"
        assert len(triage.uncertainties) == 0

    def test_22_23_24_mandatory_uncertainty_and_conflicting_evidence_preserved(self):
        # 22. Low confidence audio alert
        incident_low = SecurityIncidentDTO(
            incident_id="inc_audio_low",
            title="Possible Voice Scam",
            incident_type="VOICE_SCAM_INCIDENT",
            severity="MEDIUM",
            confidence="PROBABILISTIC",
        )
        alert_low = SOCAlertDTO(
            alert_id="alt_a_low",
            title="Probabilistic Voice Clone Match",
            category="VOICE_SCAM",
            confidence="PROBABILISTIC",
        )
        triage_low = IncidentTriageEngine.triage_incident(incident_low, [alert_low], is_conflicted_evidence=True)
        assert any("probabilistic" in u.lower() for u in triage_low.uncertainties)
        # 23. Conflicted intelligence
        assert any("conflicting" in u.lower() for u in triage_low.uncertainties)
        # 24. Missing evidence
        assert any("missing" in u.lower() for u in triage_low.uncertainties)
